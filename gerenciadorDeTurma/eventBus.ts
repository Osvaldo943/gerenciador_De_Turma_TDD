type EventHandler = (payload: any) => void;

class EventBus {
  private handlers = new Map<string, EventHandler[]>();

  subscribe(event: string, handler: EventHandler) {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, []);
    }

    this.handlers.get(event)?.push(handler);
  }

  publish(event: string, payload: any) {
    const handlers = this.handlers.get(event);

    if (handlers) {
      for (const handler of handlers) {
        handler(payload);
      }
    }
  }
}

export const eventBus = new EventBus();
