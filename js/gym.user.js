// ==UserScript==
// @name         Gym scraper
// @namespace    yata.alwaysdata.net
// @version      1.0
// @updateURL    https://github.com/Kivou-2000607/gym-formula/raw/master/js/gym.user.js
// @description  export gym training data in order to crack the formula
// @author       Pyrit[2111649]
// @match        https://www.torn.com/gym.php
// @grant        GM.xmlHttpRequest
// @grant        GM.getValue
// @grant        GM.setValue
// @run-at       document-start
// ==/UserScript==

const apiKey = "";

const state = {
    counter: 0,
    lastUpdate: Number.MAX_SAFE_INTEGER,
    initialHappy: [],
    updatedHappy: [],
    responses: [],
    api: undefined,
};

function handleApiResponse(response) {
    if (response.status != 200) {
        return response;
    }
    const data = JSON.parse(response.responseText);
    if (!("error" in data)) {
        return response;
    }
    const error = data["error"];
    const code = error["code"];
    response.responseText = error.error.error;

    if ([1, 2, 3, 4, 6].includes(code)) response.status = 400;
    else if ([0, 12].includes(code)) response.status = 500;
    else if ([7, 8, 10, 11].includes(code)) response.status = 403;
    else if ([9].includes(code)) response.status = 503;
    else if ([5].includes(code)) response.status = 429;
    return response;
}

const getIdentifier = () =>
    GM.getValue("gym_formula_id").then((id) => {
        if (id === undefined) {
            const arr = new Uint8Array(8);
            crypto.getRandomValues(arr);
            id = btoa(
                Array.prototype.map.call(arr, (byte) =>
                    String.fromCharCode(byte)
                )
            );
            GM.setValue("gym_formula_id", id);
        }
        return id;
    });

const getApiData = () =>
    new Promise((resolve, reject) => {
        if (apiKey === "") reject("You haven't entered your API key");

        if (state.api) resolve(state.api);

        getIdentifier().then((id) =>
            GM.xmlHttpRequest({
                url: `https://api.torn.com/user/?key=${apiKey}&selections=perks,timestamp`,
                onload: (response) => {
                    console.log(response);
                    response = handleApiResponse(response);
                    if (response.status != 200) {
                        reject(
                            `HTTP Status ${response.status} ${response.statusText}: ${response.responseText}`
                        );
                        return;
                    }
                    const perkRegex = /gym|gain|happ/i;
                    const json = JSON.parse(response.responseText);
                    state.api = {
                        faction_perks: json.faction_perks?.filter((perk) =>
                            perkRegex.test(perk)
                        ),
                        company_perks: json.company_perks?.filter((perk) =>
                            perkRegex.test(perk)
                        ),
                        enhancer_perks: json.enhancer_perks?.filter((perk) =>
                            perkRegex.test(perk)
                        ),
                        education_perks: json.education_perks?.filter((perk) =>
                            perkRegex.test(perk)
                        ),
                        property_perks: json.property_perks?.filter((perk) =>
                            perkRegex.test(perk)
                        ),
                        book_perks: json.book_perks?.filter((perk) =>
                            perkRegex.test(perk)
                        ),
                        time_diff: Math.floor(
                            Date.now() / 1000 - json.timestamp
                        ),
                        id_key: id,
                    };
                    resolve(state.api);
                },
            })
        );
    });

const displayMessage = (message) => {
    const messageElement = document.createElement("div");
    messageElement.innerHTML = `
        <div class="info-msg-cont border-round ${message.color}" style="display:block">
            <div class="info-msg border-round">
                <i class="info-icon"></i>
                <div class="delimiter">
                    <div class="msg right-round">
                        <div class="ajax-action">
                            gym formula script: ${message.content}
                        </div>
                    </div>
                </div>
            </div>
        </div>`;

    console.log("insert", messageElement);

    document
        .querySelector(".content-wrapper")
        .insertBefore(messageElement, document.querySelector("#gymroot"));
};

const resetState = () => {
    state.counter = 0;
    state.lastUpdate = Number.MAX_SAFE_INTEGER;
    state.initialHappy = [];
    state.updatedHappy = [];
    state.responses = [];
};

const announceRequest = (happy) => {
    state.initialHappy.push(happy);

    return state.counter++;
};

const happyUpdate = (happy) => {
    if (state.counter === 0) return;

    if (happy > state.lastUpdate) {
        resetState();
        return;
    }

    state.updatedHappy.push(happy);
    state.lastUpdate = happy;

    sendData();
};

const publishResponse = (response) => {
    if (state.counter === 0) return;

    state.responses.push(response);

    sendData();
};

const sendData = () => {
    if (
        state.counter > state.responses.length ||
        state.counter > state.updatedHappy.length
    )
        return;

    const happyAfter = state.updatedHappy.sort((a, b) => b - a);

    const maxHappy = Math.max(...state.initialHappy);
    let happyBefore = [];
    happyAfter.forEach((happy, pos) => {
        if (pos === 0) {
            happyBefore[pos] = maxHappy;
        } else {
            happyBefore[pos] = happyAfter[pos - 1];
        }
    });

    const payload = state.responses
        .sort((a, b) => a.stat_after - b.stat_after)
        .map((response, pos) => ({
            ...response,
            happy_before: happyBefore[pos],
            happy_after: happyAfter[pos],
        }));

    resetState();

    getApiData()
        .then((api) => {
            console.log({ payload, api });

            GM.xmlHttpRequest({
                url: "https://yata.alwaysdata.net/api/gym",
                method: "POST",
                headers: {
                    "content-type": "application/json",
                },
                data: JSON.stringify({ payload, api }),
                onload: (response) => console.log(response),
            });
            // What should we do in case of API Errors?
        })
        .catch((error) => displayMessage({ content: error, color: "red" }));
};

const getHappy = () =>
    parseInt(
        document
            .querySelector("#barHappy > div > p:nth-child(2)")
            .innerText.match(/^\d+/)[0]
    );

const getGym = () => {
    const id = [...document.querySelectorAll('[id^="gym"]')]
        .filter((gym) =>
            [...gym.classList].some((cls) => cls.indexOf("active") !== -1)
        )
        .map((active) => parseInt(active.id.match(/\d+$/)[0]))[0];

    return id > 0 ? id : 33;
};

const fetch = window.fetch;

unsafeWindow.fetch = function () {
    if (arguments[0].indexOf("gym.php?step=train") === -1) {
        return fetch.apply(this, arguments);
    }
    announceRequest(getHappy());
    return new Promise((resolve, reject) => {
        fetch
            .apply(this, arguments)
            .then((response) => {
                resolve(response.clone());
                response.json().then((json) => {
                    publishResponse({
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
        if (happy !== undefined) {
            happyUpdate(happy);
        }
    });
    return ws;
}.bind();
