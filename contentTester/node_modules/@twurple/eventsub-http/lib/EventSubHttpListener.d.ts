import { type EventSubListener } from '@twurple/eventsub-base';
import { type ConnectionAdapter } from './adapters/ConnectionAdapter';
import { EventSubHttpBase, type EventSubHttpBaseConfig } from './EventSubHttpBase';
/**
 * Certificate data used to make the listener server SSL capable.
 */
export interface EventSubHttpListenerCertificateConfig {
    /**
     * The private key of your SSL certificate.
     */
    key: string;
    /**
     * Your full SSL certificate chain, including all intermediate certificates.
     */
    cert: string;
}
/**
 * Configuration for an EventSub HTTP listener.
 *
 * @inheritDoc
 */
export interface EventSubHttpListenerConfig extends EventSubHttpBaseConfig {
    /**
     * The connection adapter responsible for the configuration of the connection method.
     */
    adapter: ConnectionAdapter;
}
/**
 * An HTTP listener for the Twitch EventSub event distribution mechanism.
 *
 * @hideProtected
 * @inheritDoc
 *
 * @meta category main
 */
export declare class EventSubHttpListener extends EventSubHttpBase implements EventSubListener {
    /**
     * Creates a new EventSub HTTP listener.
     *
     * @param config
     *
     * @expandParams
     */
    constructor(config: EventSubHttpListenerConfig);
    /**
     * Starts the HTTP listener.
     */
    start(): void;
    /**
     * Stops the HTTP listener.
     */
    stop(): void;
    protected getHostName(): Promise<string>;
    protected getPathPrefix(): Promise<string | undefined>;
}
//# sourceMappingURL=EventSubHttpListener.d.ts.map