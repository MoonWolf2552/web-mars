import flask
from flask import jsonify, request

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(rules=(
                    '-user.jobs', '-user.departments', '-team_leader.jobs',
                    '-team_leader.departments'))
                    for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job': job.to_dict(rules=(
                '-user.jobs', '-user.departments', '-team_leader.jobs', '-team_leader.departments'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()

    job = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size']
    )

    if 'id' in request.json:
        if db_sess.query(Jobs).get(request.json['id']):
            return jsonify({'error': ' id already exists'})
        job.id = request.json['id']
    if 'collaborators' in request.json:
        job.collaborators = request.json['collaborators']
    if 'start_date' in request.json:
        job.start_date = request.json['start_date']
    if 'end_date' in request.json:
        job.end_date = request.json['end_date']
    if 'is_finished' in request.json:
        job.is_finished = request.json['is_finished']
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    db_sess = db_session.create_session()

    if not db_sess.query(Jobs).get(job_id):
        return jsonify({'error': 'Not found'})

    job = db_sess.query(Jobs).get(job_id)

    if 'team_leader' in request.json:
        job.team_leader = request.json['team_leader']
    if 'job' in request.json:
        job.job = request.json['job']
    if 'work_size' in request.json:
        job.work_size = request.json['work_size']
    if 'collaborators' in request.json:
        job.collaborators = request.json['collaborators']
    if 'start_date' in request.json:
        job.start_date = request.json['start_date']
    if 'end_date' in request.json:
        job.end_date = request.json['end_date']
    if 'is_finished' in request.json:
        job.is_finished = request.json['is_finished']

    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_news(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})