/// <reference types="node" />
import type * as http from 'http';
import type { EventSubHttpListenerCertificateConfig } from '../EventSubHttpListener';
import { ConnectionAdapter } from './ConnectionAdapter';
/**
 * The configuration of the simple connection adapter.
 */
export interface DirectConnectionAdapterConfig {
    /**
     * The host name the server is available under.
     */
    hostName: string;
    /**
     * The SSL keychain that should be used to make the server available using a secure connection.
     */
    sslCert: EventSubHttpListenerCertificateConfig;
}
/**
 * A WebHook connection adapter that enables a direct connection.
 *
 * Requires the server to be directly available to the internet.
 *
 * @hideProtected
 *
 * @meta category adapters
 */
export declare class DirectConnectionAdapter extends ConnectionAdapter {
    private readonly _hostName;
    /**
     * Creates a new simple WebHook adapter.
     *
     * @expandParams
     *
     * @param options
     */
    constructor(options: DirectConnectionAdapterConfig);
    /**
     * Updates the SSL certificate, for example if the old one is expired.
     *
     * @expandParams
     *
     * @param ssl The new certificate data.
     */
    updateSslCertificate(ssl: EventSubHttpListenerCertificateConfig): void;
    /** @protected */
    createHttpServer(): http.Server;
    /** @protected */
    get listenUsingSsl(): boolean;
    /** @protected */
    getHostName(): Promise<string>;
}
//# sourceMappingURL=DirectConnectionAdapter.d.ts.map