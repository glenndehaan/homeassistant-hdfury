/**
 * Import base packages
 */
const fs = require('fs');
const express = require('express');

/**
 * Setup Express app
 */
const app = express();

/**
 * Output Device
 */
console.log(`[HDFury] Device: ${process.env.HDFURY_DEVICE}`);

/**
 * Trust proxy
 */
app.enable('trust proxy');

/**
 * Request logger
 */
app.use((req, res, next) => {
    console.log(`[Web]: ${req.originalUrl}`);
    next();
});

/**
 * Configure routers
 */
app.get('/', (req, res) => {
    res.set('Content-Type', 'text/html').send('OK');
});
app.get('/ssi/brdinfo.ssi', (req, res) => {
    res.set('Content-Type', 'text/html').send(fs.readFileSync(`${__dirname}/${process.env.HDFURY_DEVICE}/brdinfo.json`, 'utf8'));
});
app.get('/ssi/confpage.ssi', (req, res) => {
    res.set('Content-Type', 'text/html').send(fs.readFileSync(`${__dirname}/${process.env.HDFURY_DEVICE}/confpage.json`, 'utf8'));
});
app.get('/ssi/infopage.ssi', (req, res) => {
    res.set('Content-Type', 'text/html').send(fs.readFileSync(`${__dirname}/${process.env.HDFURY_DEVICE}/infopage.json`, 'utf8'));
});

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
app.listen(3000, '0.0.0.0', () => {
    console.log(`[App] Running on: 0.0.0.0:3000`);
});
