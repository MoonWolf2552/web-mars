import flask
from flask import jsonify, request

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_news():
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


@blueprint.route('/api/job/<int:job_id>', methods=['GET'])
def get_one_news(job_id):
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
