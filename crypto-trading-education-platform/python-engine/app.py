from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from tasks.backtest_task import run_backtest_task
from celery.result import AsyncResult

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])

@app.route('/health', methods=['GET'])
def health_check():
    """Health check for the Python engine."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'Python backtest engine is ready'
    })

@app.route('/backtest/run', methods=['POST'])
def run_backtest():
    """Run a backtest for a given strategy."""
    try:
        data = request.get_json()
        required_fields = ['strategy', 'symbol', 'timeframe', 'start_date', 'end_date', 'initial_capital']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        task = run_backtest_task.delay(
            strategy_config=data['strategy'],
            symbol=data['symbol'],
            timeframe=data['timeframe'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            initial_capital=data['initial_capital']
        )

        return jsonify({'task_id': task.id}), 202

    except Exception as e:
        return jsonify({'error': f'Error starting backtest: {str(e)}'}), 500

@app.route('/backtest/<task_id>/status', methods=['GET'])
def get_backtest_status(task_id):
    """Get the status of a backtest task."""
    task = AsyncResult(task_id)
    response = {
        'task_id': task_id,
        'status': task.status,
        'result': None
    }
    if task.status == 'SUCCESS':
        response['result'] = task.result
    elif task.status == 'FAILURE':
        response['result'] = str(task.info)  # Get the exception
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
