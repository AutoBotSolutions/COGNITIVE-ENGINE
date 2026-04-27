// Cognitive Engine Dashboard - Real-time Renderer

class CognitiveDashboard {
    constructor() {
        this.ws = null;
        this.events = [];
        this.thoughts = new Map();
        this.stats = {
            totalThoughts: 0,
            iterations: 0,
            memoryEntries: 0,
            avgConfidence: 0
        };
        
        this.init();
    }
    
    init() {
        this.connectWebSocket();
        this.setupEventListeners();
    }
    
    connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.updateConnectionStatus(true);
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleEvent(data);
        };
        
        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            this.updateConnectionStatus(false);
            // Attempt reconnection after 5 seconds
            setTimeout(() => this.connectWebSocket(), 5000);
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }
    
    handleEvent(data) {
        this.events.push(data);
        
        // Update event count
        document.getElementById('event-count').textContent = `Events: ${this.events.length}`;
        
        // Handle different event types
        switch (data.event_type) {
            case 'thought_generated':
            case 'thought_evaluated':
            case 'thought_accepted':
            case 'thought_rejected':
                this.handleThoughtEvent(data);
                break;
            case 'layer_execution':
                this.handleLayerEvent(data);
                break;
            case 'memory_update':
                this.handleMemoryEvent(data);
                break;
            case 'agent_action':
                this.handleAgentEvent(data);
                break;
            default:
                this.handleGenericEvent(data);
        }
        
        // Update event stream display
        this.updateEventStream();
    }
    
    handleThoughtEvent(data) {
        const thoughtData = data.data;
        this.thoughts.set(thoughtData.thought_id, thoughtData);
        
        // Update stats
        this.stats.totalThoughts = this.thoughts.size;
        if (thoughtData.confidence !== undefined) {
            this.stats.avgConfidence = this.calculateAvgConfidence();
        }
        
        this.updateStats();
        this.updateThoughtGraph();
    }
    
    handleLayerEvent(data) {
        const layerData = data.data;
        this.updateLayerActivity(layerData.layer, layerData.action);
    }
    
    handleMemoryEvent(data) {
        this.stats.memoryEntries++;
        this.updateStats();
    }
    
    handleAgentEvent(data) {
        this.updateLayerActivity('Agent', data.data.action);
    }
    
    handleGenericEvent(data) {
        // Handle any other event types
    }
    
    calculateAvgConfidence() {
        let total = 0;
        let count = 0;
        
        this.thoughts.forEach((thought) => {
            if (thought.confidence !== undefined) {
                total += thought.confidence;
                count++;
            }
        });
        
        return count > 0 ? (total / count).toFixed(2) : '0.00';
    }
    
    updateConnectionStatus(connected) {
        const statusEl = document.getElementById('connection-status');
        if (connected) {
            statusEl.textContent = '● Connected';
            statusEl.className = 'status-indicator connected';
        } else {
            statusEl.textContent = '● Disconnected';
            statusEl.className = 'status-indicator disconnected';
        }
    }
    
    updateStats() {
        document.getElementById('stat-thoughts').textContent = this.stats.totalThoughts;
        document.getElementById('stat-iterations').textContent = this.stats.iterations;
        document.getElementById('stat-memory').textContent = this.stats.memoryEntries;
        document.getElementById('stat-confidence').textContent = this.stats.avgConfidence;
    }
    
    updateThoughtGraph() {
        const container = document.getElementById('thought-graph');
        
        if (this.thoughts.size === 0) {
            container.innerHTML = '<div class="placeholder">Thoughts will appear here</div>';
            return;
        }
        
        let html = '<div class="thought-nodes">';
        
        this.thoughts.forEach((thought, id) => {
            const score = thought.score || 0;
            const confidence = thought.confidence || 0;
            const statusClass = this.getStatusClass(thought.status);
            
            html += `
                <div class="thought-node ${statusClass}" title="${thought.premise}">
                    <div class="thought-id">${id.substring(0, 8)}</div>
                    <div class="thought-score">Score: ${score.toFixed(2)}</div>
                    <div class="thought-confidence">Conf: ${confidence.toFixed(2)}</div>
                </div>
            `;
        });
        
        html += '</div>';
        container.innerHTML = html;
    }
    
    getStatusClass(status) {
        switch (status) {
            case 'accepted':
                return 'accepted';
            case 'rejected':
                return 'rejected';
            case 'evaluating':
                return 'evaluating';
            default:
                return 'generated';
        }
    }
    
    updateEventStream() {
        const container = document.getElementById('event-stream');
        const recentEvents = this.events.slice(-20).reverse();
        
        if (recentEvents.length === 0) {
            container.innerHTML = '<div class="placeholder">Events will appear here</div>';
            return;
        }
        
        let html = '';
        
        recentEvents.forEach((event) => {
            const time = new Date(event.timestamp).toLocaleTimeString();
            const typeClass = event.event_type.replace('_', '-');
            
            html += `
                <div class="event-item ${typeClass}">
                    <span class="event-time">${time}</span>
                    <span class="event-type">${event.event_type}</span>
                    <span class="event-data">${JSON.stringify(event.data).substring(0, 50)}...</span>
                </div>
            `;
        });
        
        container.innerHTML = html;
    }
    
    updateLayerActivity(layer, action) {
        const container = document.getElementById('layer-activity');
        
        const time = new Date().toLocaleTimeString();
        const item = document.createElement('div');
        item.className = 'activity-item';
        item.innerHTML = `
            <span class="activity-time">${time}</span>
            <span class="activity-layer">${layer}</span>
            <span class="activity-action">${action}</span>
        `;
        
        // Remove placeholder if exists
        const placeholder = container.querySelector('.placeholder');
        if (placeholder) {
            placeholder.remove();
        }
        
        container.insertBefore(item, container.firstChild);
        
        // Keep only last 20 items
        while (container.children.length > 20) {
            container.removeChild(container.lastChild);
        }
    }
    
    setupEventListeners() {
        // Add any additional event listeners here
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new CognitiveDashboard();
});
