// ==UserScript==
// @name         Gym scraper
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://www.torn.com/gym.php
// @grant        none
// ==/UserScript==

const fetch = window.fetch;

let counter = 0;
let finished = 0;

let initialHappy = [];

let updatedHappy = [];

let responses = [];

const announceRequest = (happy) => {
    initialHappy.push(happy);

    return counter++;
};

const publishResponse = (index, happy, response) => {
    responses[index] = response;
    updatedHappy[index] = happy;

    console.log(initialHappy, updatedHappy, responses);

    if (++finished === counter) {
        const guesstimatedHappy = updatedHappy.map((happy, pos) => {
            if (initialHappy[pos] === initialHappy[pos - 1]) {
                return updatedHappy[pos] - updatedHappy[pos - 1];
            } else {
                return happy - initialHappy[pos];
            }
        });

        console.log(
            responses.map((response, pos) => ({
                ...response,
                happyDiff: guesstimatedHappy[pos],
                happyAfter: updatedHappy[pos],
            }))
        );

        counter = 0;
        finished = 0;
        initialHappy = [];
        updatedHappy = [];
        responses = [];
    }
};

const getHappy = () =>
    parseInt(
        document
            .querySelector("#barHappy > div > p:nth-child(2)")
            .innerText.match(/^\d+/)[0]
    );

window.fetch = function () {
    if (arguments[0].indexOf("gym.php?step=train") !== -1) {
        const index = announceRequest(getHappy());
        return new Promise((resolve, reject) => {
            fetch
                .apply(this, arguments)
                .then((response) => {
                    resolve(response.clone());
                    response.json().then((json) => {
                        publishResponse(index, getHappy(), {
                            energySpent: json.energySpent,
                            newValue: json.stat.newValue,
                            gain: json.gainMessage.split(" ")[2],
                            stat: json.stat.name,
                        });
                    });
                })
                .catch((error) => reject(error));
        });
    } else {
        return fetch.apply(this, arguments);
    }
};
