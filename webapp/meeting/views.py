from flask import Blueprint, redirect, render_template, flash, url_for, session, request, jsonify
from flask_login import current_user, login_required
from webapp.meeting.forms import MeetingForm, ButtonForm
from webapp.user.forms import UserControlForm
from webapp.users import join_meets, update_meeting, add_meeting, paginate, owner_meetings, sub_to_meetings
from webapp.game.models import Game
from webapp.meeting.models import MeetingUser, GameMeeting
from webapp.config import GAMES_PER_PAGE
from webapp.database import db_session
from math import ceil
from datetime import date
from sqlalchemy.orm import load_only

blueprint = Blueprint('meeting', __name__, url_prefix='/meeting')


@blueprint.route('/create_meeting', methods=['POST', 'GET'])
@login_required
def create_meeting():
    """
    При GET запросе возвращает страницу для создания встречи.
    При POST запросе, в случае успешной валидации сохраняет
    новую встречу в БД.
    """
    title = 'Создание встречи'
    meeting_form = MeetingForm(request.form)

    meet_data = owner_meetings(current_user.id)
    if meet_data.count() >= 10:
        flash('Ошибка создания встречи, Вы создали слишком много встреч.')
        return render_template(
            'create_meeting.html',
            page_title=title,
            form=meeting_form,
        )

    if meeting_form.validate_on_submit():
        with db_session() as session:
            db_game = session.query(Game).filter(Game.name == meeting_form['game_name'].data).first()
            game_id = db_game.id if db_game else None
        new_meeting = GameMeeting(
            game_name=meeting_form['game_name'].data,
            owner_id=current_user.id,
            create_date=date.today(),
            number_of_players=meeting_form['number_of_players'].data,
            meeting_place=meeting_form['meeting_place'].data,
            meeting_date_time=f"{meeting_form['date_meeting'].data} {meeting_form['time_meeting'].data}",
            description=meeting_form['description'].data,
            subscribed_players=[],
            confirmed_players=[],
            game_id=game_id
        )

        if add_meeting(new_meeting):
            flash('Вы успешно создали встречу!')
            return redirect(url_for('meeting.meetings'))

        flash('Ошибка создания встречи, попробуйте повторить позже.')

    return render_template(
        'create_meeting.html',
        page_title=title,
        form=meeting_form,
    )


@blueprint.route('/edit_meet', methods=['GET', 'POST'])
@login_required
def edit_meet():
    title = f'Встреча {current_user.username}'
    buttons = ButtonForm()
    confirm_form = UserControlForm()

    if buttons.validate_on_submit:
        session['current_meet'] = (
            buttons.current_meet.data if buttons.current_meet.data
            else session['current_meet']
        )

    meeting_form = MeetingForm()
    meeting_data = join_meets(meet_id=session['current_meet'])
    meet_time = meeting_data.meeting_date_time.strftime("%H:%M:%S")
    meet_date = meeting_data.meeting_date_time.strftime("%Y-%m-%d")

    return render_template(
        'edit_meeting.html',
        page_title=title,
        form=meeting_form,
        meeting_data=meeting_data,
        meet_time=meet_time,
        meet_date=meet_date,
        confirm_form=confirm_form
    )


@blueprint.route('/user_control', methods=['GET', 'POST'])
@login_required
def user_control():
    form_control = UserControlForm()
    meeting_id = int(request.args['current_meet'])
    if form_control.validate_on_submit and form_control.submit_confirm:
        with db_session() as session:
            meeting = MeetingUser.get_meet(session, meeting_id)
            meeting.un_confirm_user() if meeting.confirmed else meeting.confirm_user()
            session.commit()

    return redirect(url_for('meeting.edit_meet'))


@blueprint.route('/submit_edit_meet', methods=['POST'])
@login_required
def submit_edit_meet():
    meeting_form = MeetingForm()
    if meeting_form.validate_on_submit:
        update_meeting(meeting_form, session['current_meet'])

    return redirect(url_for('meeting.edit_meet'))


@blueprint.route('/meetings', methods=['POST', 'GET'])
@login_required
def meetings():
    title = 'LFG'
    buttons = ButtonForm()
    page = int(request.args.get('p', 1))
    with db_session() as session:
        if buttons.validate_on_submit():
            meet_data = sub_to_meetings(current_user.id)
            if meet_data.count() >= 10:
                flash('Ошибка подписки. Вы подписаны на максимальное количество встреч')
                return redirect(url_for('meeting.meetings'))
            if buttons.submit_add_wish.data:
                meet = session.query(GameMeeting).filter(GameMeeting.id == buttons.current_meet.data).first()
                new_player = MeetingUser(
                    user_id=current_user.id,
                    meeting_id=meet.id,
                    confirmed=False,
                )
                if session.query(GameMeeting).filter(
                    MeetingUser.meeting_id == meet.id
                ).filter(
                    MeetingUser.user_id == current_user.id
                ).all():
                    pass  # СЮДА НАДО ДОБАВИТЬ ПОВЕДЕНИЕ
                else:
                    session.add(new_player)
                    session.commit()

                return redirect(url_for('meeting.meetings'))

        if buttons.submit_del.data:
            player = session.query(MeetingUser).join(GameMeeting).filter(
                GameMeeting.id == buttons.current_meet.data
            ).filter(
                MeetingUser.meeting_id == GameMeeting.id
            ).filter(MeetingUser.user_id == current_user.id).one()
            session.delete(player)
            session.commit()

            return redirect(url_for('meeting.meetings'))

        if buttons.submit_edit.data:
            return redirect(url_for('user.profile'))

            # return redirect(url_for('meeting.meetings'))

        # with db_session() as session:
        active_games = GameMeeting.active_games(session)
        query = active_games.order_by(GameMeeting.meeting_date_time.asc())
        meets_list = paginate(query, page, GAMES_PER_PAGE).all()
        last_page = ceil(active_games.count() / GAMES_PER_PAGE)
        current_user_meetings = sub_to_meetings(current_user.id)
        return render_template(
            'meetings.html',
            meets_list=meets_list,
            page_title=title,
            current_page=page,
            last_page=last_page,
            buttons=buttons,
            current_user=current_user,
            current_user_meetings=current_user_meetings
        )


@blueprint.route('/_game_info', methods=['GET'])
def game_info():
    search = request.form.get('game')
    with db_session() as session:
        return jsonify(session.query(Game).filter(Game.name.ilike(f'%{search}%')).first())


@blueprint.route('/_autocomplete', methods=['GET'])
def autocomplete():
    with db_session() as session:
        search = request.args.get('q')
        if not search:
            search = []
        games_db = session.query(Game).options(load_only('name')).filter(Game.name.ilike(f'%{search}%')).limit(15)
        games_names = [game.name for game in games_db]
        return jsonify(games_names)
