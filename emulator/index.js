/**
 * Import base packages
 */
const fs = require('fs');
const express = require('express');

/**
 * Express port start number
 */
const port = 3000;

/**
 * Define all HDFury emulated devices
 */
const devices = [
    "diva",
    "vertex2",
    "vrroom"
];

/**
 * Create express app for a device
 */
const createEmulator = (device, key) => {
    /**
     * Setup Express app
     */
    const app = express();

    /**
     * Trust proxy
     */
    app.enable('trust proxy');

    /**
     * Request logger
     */
    app.use((req, res, next) => {
        console.log(`[${device}][${req.method}]: ${req.originalUrl}`);
        next();
    });

    /**
     * Configure routers
     */
    app.get('/', (req, res) => {
        res.set('Content-Type', 'text/html').send('OK');
    });
    if(fs.existsSync(`${__dirname}/${device}/brdinfo.json`)) {
        app.get('/ssi/brdinfo.ssi', (req, res) => {
            res.set('Content-Type', 'text/html').send(fs.readFileSync(`${__dirname}/${device}/brdinfo.json`, 'utf8'));
        });
    }
    if(fs.existsSync(`${__dirname}/${device}/cecpage.json`)) {
        app.get('/ssi/cecpage.ssi', (req, res) => {
            res.set('Content-Type', 'text/html').send(fs.readFileSync(`${__dirname}/${device}/cecpage.json`, 'utf8'));
        });
    }
    if(fs.existsSync(`${__dirname}/${device}/confpage.json`)) {
        app.get('/ssi/confpage.ssi', (req, res) => {
            res.set('Content-Type', 'text/html').send(fs.readFileSync(`${__dirname}/${device}/confpage.json`, 'utf8'));
        });
    }
    if(fs.existsSync(`${__dirname}/${device}/edidpage.json`)) {
        app.get('/ssi/edidpage.ssi', (req, res) => {
            res.set('Content-Type', 'text/html').send(fs.readFileSync(`${__dirname}/${device}/edidpage.json`, 'utf8'));
        });
    }
    if(fs.existsSync(`${__dirname}/${device}/hdrpage.json`)) {
        app.get('/ssi/hdrpage.ssi', (req, res) => {
            res.set('Content-Type', 'text/html').send(fs.readFileSync(`${__dirname}/${device}/hdrpage.json`, 'utf8'));
        });
    }
    if(fs.existsSync(`${__dirname}/${device}/infopage.json`)) {
        app.get('/ssi/infopage.ssi', (req, res) => {
            res.set('Content-Type', 'text/html').send(fs.readFileSync(`${__dirname}/${device}/infopage.json`, 'utf8'));
        });
    }

    /**
     * Setup default 404 message
     */
    app.use((req, res) => {
        res.status(404);
        res.send('Not Found!');
    });

    /**
     * Disable powered by header for security reasons
     */
    app.disable('x-powered-by');

    /**
     * Start listening on port
     */
    app.listen(port + key, '0.0.0.0', () => {
        console.log(`[App] Running on: 0.0.0.0:${port + key} (HDFury Device: ${device})`);
    });
}

/**
 * Setup emulators for all devices
 */
devices.forEach((device, key) => {
    createEmulator(device, key);
});
