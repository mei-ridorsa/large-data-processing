#!/usr/bin/env python
import os
import threading
import uuid

import click
from flask import jsonify, send_from_directory

from app import create_app, db, models, forms
from app.csv_processor import process
from config import base_dir

app = create_app()


@app.route('/api/v1/reports/process/<filename>', methods=['POST'])
def process_report(filename):
    task_id = uuid.uuid4().hex

    def long_running_task(**kwargs):
        params = kwargs.get('post_data', {})
        process(params[0], params[1])

    thread = threading.Thread(target=long_running_task, kwargs={
        'post_data': [filename, task_id]})
    thread.start()

    response = {'message': 'success', 'report_id': task_id}
    return jsonify(response)


@app.route('/api/v1/reports/<report_id>', methods=['GET'])
def get_report(report_id):
    if not os.path.exists(os.path.join(base_dir, 'output', report_id + '.csv')):
        return jsonify({'message': 'The report does not exist. Please check that the id is correct or try again later',
                        'report_id': report_id})

    return send_from_directory(os.path.join(base_dir, 'output'), report_id + '.csv')


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, models=models, forms=forms)


@app.cli.command()
def create_db():
    """Create the configured database."""
    db.create_all()


@app.cli.command()
@click.confirmation_option(prompt='Drop all database tables?')
def drop_db():
    """Drop the current database."""
    db.drop_all()


if __name__ == '__main__':
    app.run()
