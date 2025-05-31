function analyzeTeam() {
  const teamId = document.getElementById("teamId").value.trim();
  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "";

  if (!teamId) {
    resultDiv.textContent = "Пожалуйста, введите ID команды.";
    return;
  }

  let wins = 0;
  let losses = 0;
  let draws = 0;
  let goalsFor = 0;
  let goalsAgainst = 0;
  let playedMatches = 0;

  matches.forEach(match => {
    const isTeam1 = match.team1_id.toString() === teamId;
    const isTeam2 = match.team2_id.toString() === teamId;

    if (!isTeam1 && !isTeam2) return;

    let teamGoals = isTeam1 ? match.team1_score : match.team2_score;
    let opponentGoals = isTeam1 ? match.team2_score : match.team1_score;

    goalsFor += teamGoals;
    goalsAgainst += opponentGoals;
    playedMatches++;

    if (teamGoals > opponentGoals) wins++;
    else if (teamGoals < opponentGoals) losses++;
    else draws++;
  });

  if (playedMatches === 0) {
    resultDiv.textContent = "Матчи с участием этой команды не найдены.";
    return;
  }

  resultDiv.innerHTML = `
    <h3>Статистика команды ${teamId}:</h3>
    <ul>
      <li>Всего матчей: ${playedMatches}</li>
      <li>Побед: ${wins}</li>
      <li>Поражений: ${losses}</li>
      <li>Ничьих: ${draws}</li>
      <li>Забито голов: ${goalsFor}</li>
      <li>Пропущено голов: ${goalsAgainst}</li>
    </ul>
  `;
}
