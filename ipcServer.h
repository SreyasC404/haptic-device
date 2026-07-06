#ifndef IPC_SERVER_H
#define IPC_SERVER_H

// Starts a background thread that listens on 127.0.0.1:<port> for plain-text
// control commands sent by the desktop launcher UI. If the port cannot be
// bound, a warning is printed and the simulation continues without remote
// control (mouse/keyboard/haptic device input still works normally).
void startIpcServer(int port);

// Signals the IPC listener thread to stop and blocks until it has exited.
// Safe to call even if the server was never started.
void stopIpcServer();

#endif // IPC_SERVER_H
