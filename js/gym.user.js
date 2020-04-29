// ==UserScript==
// @name         Gym scraper
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       Pyrit[2111649]
// @match        https://www.torn.com/gym.php
// @grant        GM.xmlHttpRequest
// @run-at       document-start
// ==/UserScript==

const state = {
    counter: 0,
    lastUpdate: Number.MAX_SAFE_INTEGER,
    initialHappy: [],
    updatedHappy: [],
    responses: [],
};

const resetState = () => {
    state.counter = 0;
    state.lastUpdate = Number.MAX_SAFE_INTEGER;
    state.initialHappy = [];
    state.updatedHappy = [];
    state.responses = [];
};

const happyUpdate = (happy) => {
    if (state.counter > 0) {
        if (happy < state.lastUpdate) {
            state.updatedHappy.push(happy);
            state.lastUpdate = happy;
        } else {
            resetState();
        }
    }
};

const announceRequest = (happy) => {
    state.initialHappy.push(happy);

    return state.counter++;
};

const publishResponse = (index, response) => {
    if (state.counter === 0) return;

    state.responses[index] = response;

    if (state.counter <= state.updatedHappy.length) {
        const happyAfter = state.updatedHappy.sort().reverse();

        const maxHappy = Math.max(...state.initialHappy);
        let happyBefore = [];
        happyAfter.forEach((happy, pos) => {
            if (pos === 0) {
                happyBefore[pos] = maxHappy;
            } else {
                happyBefore[pos] =
                    maxHappy + happyAfter[pos - 1] - happyBefore[pos - 1];
            }
        });

        console.log(
            state.responses.map((response, pos) => ({
                ...response,
                happyBefore: happyBefore[pos],
                happyAfter: happyAfter[pos],
            }))
        );

        GM.xmlHttpRequest({
            url: "https://yata.alwaysdata.net/tmp/gym",
            method: "POST",
            headers: {
                "content-type": "application/json",
            },
            body: JSON.stringify(
                state.responses.map((response, pos) => ({
                    ...response,
                    happy_before: happyBefore[pos],
                    happy_after: happyAfter[pos],
                }))
            ),
            onload: (response) => console.log(response),
        });

        resetState();
    }
};

const getHappy = () =>
    parseInt(
        document
            .querySelector("#barHappy > div > p:nth-child(2)")
            .innerText.match(/^\d+/)[0]
    );

const getGym = () =>
    [...document.querySelectorAll('[id^="gym"]')]
        .filter((gym) =>
            [...gym.classList].some((cls) => cls.indexOf("active") !== -1)
        )
        .map((active) => parseInt(active.id.match(/\d+$/)[0]))[0];

const fetch = window.fetch;

unsafeWindow.fetch = function () {
    if (arguments[0].indexOf("gym.php?step=train") !== -1) {
        const index = announceRequest(getHappy());
        return new Promise((resolve, reject) => {
            fetch
                .apply(this, arguments)
                .then((response) => {
                    resolve(response.clone());
                    response.json().then((json) => {
                        publishResponse(index, {
                            energy_used: json.energySpent,
                            stat_after: parseFloat(
                                json.stat.newValue.replace(/,/g, "")
                            ),
                            stat_gain: parseFloat(
                                json.gainMessage.split(" ")[2].replace(/,/g, "")
                            ),
                            stat_type: json.stat.name,
                            gym_id: getGym(),
                        });
                    });
                })
                .catch((error) => reject(error));
        });
    } else {
        return fetch.apply(this, arguments);
    }
};

const OrigWebSocket = window.WebSocket;
const callWebSocket = OrigWebSocket.apply.bind(OrigWebSocket);
let wsAddListener = OrigWebSocket.prototype.addEventListener;
wsAddListener = wsAddListener.call.bind(wsAddListener);
unsafeWindow.WebSocket = function WebSocket(url, protocols) {
    let ws;
    if (!(this instanceof WebSocket)) {
        // Called without 'new' (browsers will throw an error).
        ws = callWebSocket(this, arguments);
    } else if (arguments.length === 1) {
        ws = new OrigWebSocket(url);
    } else if (arguments.length >= 2) {
        ws = new OrigWebSocket(url, protocols);
    } else {
        // No arguments (browsers will throw an error)
        ws = new OrigWebSocket();
    }
    window.WebSocket.prototype = OrigWebSocket.prototype;
    window.WebSocket.prototype.constructor = window.WebSocket;

    wsAddListener(ws, "message", (event) => {
        const packet = JSON.parse(event.data);
        const happy =
            packet.body?.data?.message?.namespaces?.sidebar?.actions
                ?.updateHappy?.amount;
        if (happy) {
            happyUpdate(happy);
        }
    });
    return ws;
}.bind();
