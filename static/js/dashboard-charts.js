(() => {
  const dataNode = document.getElementById('dashboard-chart-data');
  if (!dataNode) return;
  const charts = JSON.parse(dataNode.textContent);
  document.querySelectorAll('.farm-chart').forEach((canvas) => {
    const chart = charts[canvas.dataset.chart];
    const ctx = canvas.getContext('2d'); const width = canvas.clientWidth || 420; const height = 230;
    canvas.width = width * devicePixelRatio; canvas.height = height * devicePixelRatio; canvas.style.height = `${height}px`; ctx.scale(devicePixelRatio, devicePixelRatio);
    if (!chart.values.length) { ctx.fillStyle = '#64748b'; ctx.font = '14px system-ui'; ctx.fillText('Add expenses to see your graph.', 24, 116); return; }
    const max = Math.max(...chart.values, 1); const pad = {l: 42, r: 14, t: 20, b: 52}; const usableW = width - pad.l - pad.r; const usableH = height - pad.t - pad.b;
    ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 1; for (let i=0;i<=4;i++) { const y=pad.t+usableH*i/4; ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(width-pad.r,y);ctx.stroke(); }
    const slot=usableW/chart.values.length; chart.values.forEach((value,i) => { const barW=Math.min(42,slot*.62); const barH=usableH*(value/max); const x=pad.l+i*slot+(slot-barW)/2; const y=pad.t+usableH-barH; const gradient=ctx.createLinearGradient(0,y,0,y+barH); gradient.addColorStop(0,'#22c55e');gradient.addColorStop(1,'#15803d');ctx.fillStyle=gradient;ctx.fillRect(x,y,barW,barH);ctx.fillStyle='#475569';ctx.font='11px system-ui';ctx.textAlign='center';ctx.fillText(chart.labels[i].slice(0,11),x+barW/2,height-25); });
    ctx.fillStyle='#64748b';ctx.font='11px system-ui';ctx.textAlign='left';ctx.fillText(`₹${max.toLocaleString()}`,2,pad.t+5);ctx.fillText('₹0',10,pad.t+usableH);
  });
})();
