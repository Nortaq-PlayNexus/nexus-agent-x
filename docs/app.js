// NEXUS UI — stub for Tauri/React. Connect to EventBus via WebSocket.
// In production: ws://127.0.0.1:8000/events
const bus = new EventSource('/events');
if (bus) bus.onmessage = e => console.log('event', JSON.parse(e.data));
console.log('NEXUS UI loaded — ULTRA spec §62-65');
