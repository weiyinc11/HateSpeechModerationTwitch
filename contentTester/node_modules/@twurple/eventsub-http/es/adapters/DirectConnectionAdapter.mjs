import { __decorate } from "tslib";
import { Enumerable } from '@d-fischer/shared-utils';
import { rtfm } from '@twurple/common';
import * as https from 'https';
import { checkHostName } from "../checks.mjs";
import { ConnectionAdapter } from "./ConnectionAdapter.mjs";
/**
 * A WebHook connection adapter that enables a direct connection.
 *
 * Requires the server to be directly available to the internet.
 *
 * @hideProtected
 *
 * @meta category adapters
 */
let DirectConnectionAdapter = class DirectConnectionAdapter extends ConnectionAdapter {
    /**
     * Creates a new simple WebHook adapter.
     *
     * @expandParams
     *
     * @param options
     */
    constructor(options) {
        super();
        checkHostName(options.hostName);
        this._hostName = options.hostName;
        this._ssl = options.sslCert;
    }
    /**
     * Updates the SSL certificate, for example if the old one is expired.
     *
     * @expandParams
     *
     * @param ssl The new certificate data.
     */
    updateSslCertificate(ssl) {
        var _a;
        this._ssl = ssl;
        (_a = this._httpsServer) === null || _a === void 0 ? void 0 : _a.setSecureContext(ssl);
    }
    /** @protected */
    createHttpServer() {
        return (this._httpsServer = https.createServer({
            key: this._ssl.key,
            cert: this._ssl.cert,
        }));
    }
    /** @protected */
    // eslint-disable-next-line @typescript-eslint/class-literal-property-style
    get listenUsingSsl() {
        return true;
    }
    /** @protected */
    async getHostName() {
        return this._hostName;
    }
};
__decorate([
    Enumerable(false)
], DirectConnectionAdapter.prototype, "_ssl", void 0);
__decorate([
    Enumerable(false)
], DirectConnectionAdapter.prototype, "_httpsServer", void 0);
DirectConnectionAdapter = __decorate([
    rtfm('eventsub-http', 'DirectConnectionAdapter')
], DirectConnectionAdapter);
export { DirectConnectionAdapter };
