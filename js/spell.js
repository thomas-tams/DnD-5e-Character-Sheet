// At the top of spell.js OR in a dedicated globals.js loaded before all
window.pinnedSpells = window.pinnedSpells || [];

$(document).ready(function () {
    let spells = [];

    // Load spells from spell.json
    $.getJSON('data/spells.json?nocache=' + new Date().getTime(), function (data) {
        spells = data;
    });

    // Search for spells
    $('#spell-search-input').on('input', function () {
        const query = $(this).val().toLowerCase();
        const results = spells.filter(spell => spell.spell_name.toLowerCase().includes(query));
        displaySpellResults(results);
    });

    // Display search results
    function displaySpellResults(results) {
        const resultsContainer = $('#spell-results');
        resultsContainer.empty();
        results.forEach(spell => {
            const spellElement = $(`
                <div class="spell-result w3-card w3-padding w3-margin-bottom">
                    <span>${spell.spell_name}</span>
                    <button class="w3-button w3-blue-gray w3-round pin-spell" data-spell="${spell.spell_name}">Pin</button>
                </div>
            `);
            spellElement.find('.pin-spell').on('click', function () {
                pinSpell(spell);
            });
            resultsContainer.append(spellElement);
        });
    }

    // Pin a spell
    function pinSpell(spell) {
        if (!window.pinnedSpells.includes(spell)) {
            window.pinnedSpells.push(spell);
            displayPinnedSpells();
        }
    }

    // Display pinned spells
    function displayPinnedSpells() {
        const pinnedContainer = $('#pinned-spells');
        pinnedContainer.empty();

        window.pinnedSpells.forEach(spell => {
            const spellElement = $(`
                <div class="pinned-spell w3-card w3-padding w3-margin-bottom">
                    <table class="w3-table-all">
                        <tr>
                            <th>Key</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Name</td>
                            <td>${spell.spell_name}</td>
                        </tr>
                        <tr>
                            <td>Level</td>
                            <td>${spell.spell_level}</td>
                        </tr>
                        <tr>
                            <td>Type</td>
                            <td>${spell.spell_type}</td>
                        </tr>
                        <tr>
                            <td>Classes</td>
                            <td>${spell.spell_user_classes.join(', ')}</td>
                        </tr>
                        <tr>
                            <td>Casting Time</td>
                            <td>${spell.casting_time}</td>
                        </tr>
                        <tr>
                            <td>Range</td>
                            <td>${spell.range}</td>
                        </tr>
                        <tr>
                            <td>Components</td>
                            <td>${spell.components}</td>
                        </tr>
                        <tr>
                            <td>Duration</td>
                            <td>${spell.duration}</td>
                        </tr>
                        <tr>
                            <td>Description</td>
                            <td>${spell.description.replace(/\n/g, '<br>')}</td>
                        </tr>
                    </table>
                    <button class="w3-button w3-red w3-round unpin-spell" data-spell="${spell.spell_name}">Unpin</button>
                </div>
            `);

            spellElement.find('.unpin-spell').on('click', function () {
                unpinSpell(spell);
            });

            pinnedContainer.append(spellElement);
        });
    }

    // Unpin a spell
    function unpinSpell(spell) {
        window.pinnedSpells = window.pinnedSpells.filter(s => s.spell_name !== spell.spell_name);
        displayPinnedSpells();
    }
});