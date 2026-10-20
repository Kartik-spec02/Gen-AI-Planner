const form = document.getElementById('briefForm');
const result = document.getElementById('result');
const status = document.getElementById('status');
const generateBtn = document.getElementById('generateBtn');
const btnText = document.querySelector('.btn-text');

// Skeleton HTML for the loading state
const skeletonHTML = `
  <div class="skeleton-banner shimmer"></div>
  <div class="skeleton-summary shimmer"></div>
  <h3>💰 Budget Breakdown</h3>
  <div class="skeleton-table shimmer"></div>
  <h3>🗓 Timeline</h3>
  <div class="skeleton-card shimmer"></div>
  <div class="skeleton-card shimmer"></div>
  <h3>✅ Vendor Checklist</h3>
  <div class="skeleton-card shimmer"></div>
  <div class="skeleton-card shimmer"></div>
`;

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  // Show loading state immediately
  generateBtn.disabled = true;
  btnText.textContent = 'Consulting AI...';
  status.textContent = '✨ Painting your vision...';
  
  // Show skeleton loader
  result.hidden = false;
  result.innerHTML = skeletonHTML;
  result.scrollIntoView({behavior: 'smooth', block: 'start'});

  const data = Object.fromEntries(new FormData(form));
  data.budget = parseFloat(data.budget);
  data.guests = parseInt(data.guests, 10);

  try {
    const res = await fetch('/api/plan', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    
    if (!res.ok) throw new Error('Failed to generate plan');
    
    const plan = await res.json();
    render(plan, data.theme);
    
    generateBtn.disabled = false;
    btnText.textContent = 'Generate Plan ✨';
    status.textContent = '';
    
  } catch (error) {
    result.hidden = true;
    status.textContent = '❌ Error generating plan.';
    generateBtn.disabled = false;
    btnText.textContent = 'Generate Plan ✨';
    console.error(error);
  }
});

function render(plan, theme) {
  // Generate real AI image using Pollinations
  const prompt = encodeURIComponent(`${theme} event planning aesthetic high quality photography`);
  const imageUrl = `https://image.pollinations.ai/prompt/${prompt}?width=1000&height=300&nologo=true`;

  const safeNotes = (text) => text ? text : '';

  result.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;">
      <h2 style="margin: 0;">Your Plan</h2>
      <button onclick="window.print()" style="margin: 0; padding: 0.6rem 1.2rem; font-size: 0.95rem; width: auto; background: #fff; color: var(--text-dark); border: 1px solid #e5e7eb; box-shadow: none;">🖨️ Print / Save PDF</button>
    </div>

    <!-- AI Image Banner -->
    <img src="${imageUrl}" class="event-image" alt="AI generated event theme" onerror="this.style.display='none'">
    
    <p class="summary">${plan.summary}</p>

    <h3>💰 Budget Breakdown</h3>
    <table>
      <tr><th>Category</th><th>%</th><th>Amount</th><th>Notes</th></tr>
      ${plan.budget_breakdown.map(b =>
        `<tr>
          <td style="font-weight: 600;">${b.category}</td>
          <td>${b.percent}%</td>
          <td style="color: var(--accent-primary); font-weight: 600;">$${b.amount.toLocaleString()}</td>
          <td style="color: var(--text-muted); font-size: 0.95rem;">${safeNotes(b.notes)}</td>
        </tr>`).join('')}
    </table>

    <h3>🗓 Timeline</h3>
    ${plan.timeline.map((p, index) => `
      <div class="phase" style="animation-delay: ${index * 0.1}s">
        <strong>${p.phase}</strong> <em>(${p.weeks_before} weeks before)</em>
        <ul>${p.tasks.map(t => `<li>${t}</li>`).join('')}</ul>
      </div>`).join('')}

    <h3>✅ Vendor Checklist</h3>
    ${plan.vendor_checklist.map((v, index) => `
      <div class="vendor" style="animation-delay: ${index * 0.1}s">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
          <strong>${v.vendor_type}</strong>
          <span style="color: var(--accent-primary); font-weight: 600; font-size: 1rem;">est. $${v.estimated_cost.toLocaleString()}</span>
        </div>
        <ul>${v.questions.map(q => `<li>${q}</li>`).join('')}</ul>
      </div>`).join('')}

    <h3>💡 Personalized Ideas</h3>
    <ul class="ideas">${plan.personalized_ideas.map(i => `<li>${i}</li>`).join('')}</ul>
  `;
  
  setTimeout(() => {
    result.scrollIntoView({behavior: 'smooth', block: 'start'});
  }, 100);
}