"""
Flask Web Interface for Jarvis AI Multi-Agent System
"""

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import logging
from datetime import datetime
from jarvis import JarvisAI, AgentRole

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'jarvis-secret-key-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Jarvis
jarvis = JarvisAI(name="Jarvis")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store active connections
active_users = {}


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/api/status')
def get_status():
    """Get system status"""
    try:
        status = jarvis.get_system_status()
        return jsonify({
            'success': True,
            'data': status
        })
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/agents', methods=['GET'])
def get_agents():
    """Get all agents"""
    try:
        agents = jarvis.list_all_agents()
        return jsonify({
            'success': True,
            'data': agents
        })
    except Exception as e:
        logger.error(f"Error getting agents: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/agents', methods=['POST'])
def create_agent():
    """Create a new agent"""
    try:
        data = request.json
        name = data.get('name')
        role = data.get('role', 'general')
        
        if not name:
            return jsonify({'success': False, 'error': 'Agent name required'}), 400
        
        agent_id = jarvis.create_agent(name, role)
        agent = jarvis.agent_manager.get_agent(agent_id)
        
        # Broadcast to all connected clients
        socketio.emit('agent_created', {
            'agent': agent.get_info()
        }, broadcast=True)
        
        return jsonify({
            'success': True,
            'data': agent.get_info()
        })
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/agents/<agent_id>', methods=['GET'])
def get_agent(agent_id):
    """Get specific agent details"""
    try:
        agent_info = jarvis.get_agent_status(agent_id)
        if not agent_info:
            return jsonify({'success': False, 'error': 'Agent not found'}), 404
        
        return jsonify({
            'success': True,
            'data': agent_info
        })
    except Exception as e:
        logger.error(f"Error getting agent: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/agents/<agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    """Delete an agent"""
    try:
        success = jarvis.remove_agent(agent_id)
        if not success:
            return jsonify({'success': False, 'error': 'Agent not found'}), 404
        
        socketio.emit('agent_deleted', {'agent_id': agent_id}, broadcast=True)
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error deleting agent: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/tasks/delegate', methods=['POST'])
def delegate_task():
    """Delegate a task to an agent"""
    try:
        data = request.json
        capability = data.get('capability')
        description = data.get('description')
        priority = data.get('priority', 'normal')
        
        if not capability or not description:
            return jsonify({'success': False, 'error': 'Capability and description required'}), 400
        
        success = jarvis.delegate_task(capability, description, priority)
        
        if success:
            socketio.emit('task_delegated', {
                'capability': capability,
                'description': description,
                'priority': priority,
                'timestamp': datetime.now().isoformat()
            }, broadcast=True)
        
        return jsonify({
            'success': success,
            'message': 'Task delegated successfully' if success else 'Failed to delegate task'
        })
    except Exception as e:
        logger.error(f"Error delegating task: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/agents/message', methods=['POST'])
def send_message():
    """Send message between agents"""
    try:
        data = request.json
        from_agent_id = data.get('from_agent_id')
        to_agent_id = data.get('to_agent_id')
        message = data.get('message')
        
        if not all([from_agent_id, to_agent_id, message]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        success = jarvis.send_agent_message(from_agent_id, to_agent_id, message)
        
        if success:
            socketio.emit('message_sent', {
                'from_agent_id': from_agent_id,
                'to_agent_id': to_agent_id,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }, broadcast=True)
        
        return jsonify({'success': success})
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/agents/broadcast', methods=['POST'])
def broadcast_message():
    """Broadcast message to agents"""
    try:
        data = request.json
        agent_id = data.get('agent_id')
        message = data.get('message')
        target_role = data.get('target_role')
        
        if not agent_id or not message:
            return jsonify({'success': False, 'error': 'Agent ID and message required'}), 400
        
        count = jarvis.broadcast_to_agents(agent_id, message, target_role)
        
        socketio.emit('broadcast_sent', {
            'from_agent_id': agent_id,
            'message': message,
            'target_role': target_role,
            'recipients': count,
            'timestamp': datetime.now().isoformat()
        }, broadcast=True)
        
        return jsonify({
            'success': True,
            'recipients': count
        })
    except Exception as e:
        logger.error(f"Error broadcasting message: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/process', methods=['POST'])
def process_input():
    """Process natural language input through Jarvis"""
    try:
        data = request.json
        user_input = data.get('input')
        
        if not user_input:
            return jsonify({'success': False, 'error': 'Input required'}), 400
        
        response = jarvis.process(user_input)
        
        socketio.emit('jarvis_response', {
            'input': user_input,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }, broadcast=True)
        
        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        logger.error(f"Error processing input: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/roles')
def get_roles():
    """Get available agent roles"""
    try:
        roles = [role.value for role in AgentRole]
        return jsonify({
            'success': True,
            'data': roles
        })
    except Exception as e:
        logger.error(f"Error getting roles: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/capabilities')
def get_capabilities():
    """Get available capabilities"""
    try:
        manager = jarvis.agent_manager
        capabilities = {}
        for role, caps in manager.agent_registry.items():
            capabilities[role] = caps
        
        return jsonify({
            'success': True,
            'data': capabilities
        })
    except Exception as e:
        logger.error(f"Error getting capabilities: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# WebSocket events for real-time updates
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    user_id = request.sid
    active_users[user_id] = {
        'connected_at': datetime.now().isoformat(),
        'actions': 0
    }
    logger.info(f"Client {user_id} connected")
    emit('connection_response', {'data': 'Connected to Jarvis'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    user_id = request.sid
    if user_id in active_users:
        del active_users[user_id]
    logger.info(f"Client {user_id} disconnected")


@socketio.on('request_status')
def handle_status_request():
    """Real-time status request"""
    try:
        status = jarvis.get_system_status()
        emit('status_update', status)
    except Exception as e:
        logger.error(f"Error in status request: {e}")
        emit('error', {'message': str(e)})


@socketio.on('request_agents')
def handle_agents_request():
    """Real-time agents request"""
    try:
        agents = jarvis.list_all_agents()
        emit('agents_update', {'agents': agents})
    except Exception as e:
        logger.error(f"Error in agents request: {e}")
        emit('error', {'message': str(e)})


if __name__ == '__main__':
    logger.info("Starting Jarvis Web Interface...")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
