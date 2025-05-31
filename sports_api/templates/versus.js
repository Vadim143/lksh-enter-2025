document.getElementById('compare').addEventListener('click', comparePlayers);


async function comparePlayers() {
  const id1 = parseInt(document.getElementById('player1').value);
  const id2 = parseInt(document.getElementById('player2').value);
  const resultDiv = document.getElementById('result');
  resultDiv.innerHTML = '';

  if (isNaN(id1) || isNaN(id2)) {
    resultDiv.textContent = 'Введите оба ID игрока.';
    return;
  }
  resultDiv.textContent = 'Загрузка...';
  let count = 0;
  const relevantMatches = [];

  for (const match of matches) {
    const team1 = teamById[match.team1_id];
    const team2 = teamById[match.team2_id];
    const t1Players = team1.players;
    const t2Players = team2.players;

    const cond1 = t1Players.includes(id1) && t2Players.includes(id2);
    const cond2 = t2Players.includes(id1) && t1Players.includes(id2);

    if (cond1 || cond2) {
      count++;
      relevantMatches.push(`Матч #${match.id}: ${team1.name} (${match.team1_score}) vs ${team2.name} (${match.team2_score})`);
    }
  }

  resultDiv.innerHTML = `<p>Найдено матчей: ${count}</p>`;
  relevantMatches.forEach(m => {
    const div = document.createElement('div');
    div.textContent = m;
    resultDiv.appendChild(div);
  });
}