console.log("SCRIPT STARTED");

const { Bluetooth } = require("webbluetooth");
const { connectGanCube } = require("gan-web-bluetooth");

// gan-web-bluetooth expects navigator.bluetooth
global.navigator = {};

global.navigator.bluetooth = new Bluetooth({
  scanTime: 30,
  deviceFound: (device) => {
    const name = device?.name || "";
    console.log("FOUND:", JSON.stringify({ name, id: device?.id }, null, 0));

    // Only accept likely GAN cube names
    return /gan/i.test(name);
  },
});

const WebSocket = require("ws");
// ... keep your other requires above this line too

async function main() {
  console.log("Searching for GAN cube…");

  //const mac = process.env.GAN_MAC;
  //if (!mac) throw new Error("Set GAN_MAC to your cube MAC");

  //const conn = await connectGanCube(async () => mac);
  const conn = await connectGanCube();
  console.log("Connected!");

  // ✅ START WEBSOCKET SERVER (put this right after "Connected!")
  const wss = new WebSocket.Server({ port: 17433 });
  console.log("WebSocket listening on ws://127.0.0.1:17433");

  function broadcast(obj) {
    console.log("[bridge->ws] sending", JSON.stringify(obj));
    const msg = JSON.stringify(obj);
    for (const client of wss.clients) {
      if (client.readyState === WebSocket.OPEN) client.send(msg);
    }
  }

  wss.on("connection", (ws) => {
    ws.send(JSON.stringify({ type: "status", msg: "bridge connected" }));
  });
  // ✅ END WEBSOCKET SERVER

  // ✅ MOVE HANDLER: print + broadcast
  conn.events$.subscribe((event) => {
  if (event.type === "MOVE") {
    console.log("MOVE:", event.move);
    broadcast({ type: "move", move: event.move, t: Date.now() });
  }
});

  await conn.sendCubeCommand({ type: "REQUEST_FACELETS" });
  console.log("Ready — turn the cube");

  console.log("Listening for moves… press Ctrl+C to quit.");
  process.stdin.resume(); // keep Node alive
}

main().catch((e) => {
  console.error("Fatal error:", e);
});
