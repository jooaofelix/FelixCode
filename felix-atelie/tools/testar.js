/*
 * Teste visual do Ateliê 3D: abre o app num navegador sem janela, tira fotos da
 * tela nas três vistas (modo Foto e modo 3D) e exporta a imagem final.
 * Também lista erros do console.
 *
 * Uso (dentro de felix-atelie/tools):
 *   npm install
 *   node testar.js                 # testa ../index.html, fotos em ./capturas
 *   node testar.js ../index.html saida-teste
 *
 * As bibliotecas da CDN (three, fabric) são servidas do node_modules, então o
 * teste funciona mesmo sem internet. As fontes do Google ficam bloqueadas, então
 * os textos aparecem com fonte reserva nas capturas; isso é esperado.
 */
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const html = path.resolve(process.argv[2] || path.join(__dirname, '..', 'index.html'));
const out = path.resolve(process.argv[3] || path.join(__dirname, 'capturas'));
// procura a pasta do pacote em node_modules (sem require.resolve, que esbarra no campo "exports")
const pkgDir = (name) => {
  for (let d = __dirname; ; d = path.dirname(d)) {
    const c = path.join(d, 'node_modules', name);
    if (fs.existsSync(c)) return c;
    if (path.dirname(d) === d) throw new Error(`Instale as dependências: cd tools && npm install (faltou ${name})`);
  }
};
const lib = (p) => { const [name, ...rest] = p.split('/'); return path.join(pkgDir(name), ...rest); };

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push('erro de script: ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error' && !/ERR_FAILED|ERR_NAME|net::/.test(m.text())) errors.push('console: ' + m.text()); });
  await page.route('**/*', (r) => {
    const u = r.request().url();
    if (u.includes('/three@')) return r.fulfill({ path: lib('three/build/three.module.js'), contentType: 'text/javascript' });
    if (u.includes('/fabric@')) return r.fulfill({ path: lib('fabric/dist/fabric.min.js'), contentType: 'text/javascript' });
    if (u.startsWith('file:')) return r.continue();
    return r.abort();
  });
  await page.goto('file://' + html);
  await page.waitForTimeout(8000);
  const view = page.locator('#view3d');
  await page.screenshot({ path: path.join(out, '00-tela.png') });

  for (const mode of ['foto', '3d']) {
    await page.locator(`[data-mode="${mode}"]`).click();
    for (const v of ['front', 'side', 'back']) {
      await page.locator(`[data-view="${v}"]`).click();
      await page.waitForTimeout(2200);
      await view.screenshot({ path: path.join(out, `${mode}-${v}.png`) });
    }
  }

  await page.locator('[data-mode="foto"]').click();
  await page.locator('[data-view="front"]').click();
  await page.waitForTimeout(1200);
  await page.click('#exportPng');
  await page.waitForTimeout(2500);
  const src = await page.getAttribute('#modalImg', 'src');
  if (src && src.startsWith('data:image/png')) fs.writeFileSync(path.join(out, 'exportado.png'), Buffer.from(src.split(',')[1], 'base64'));
  else errors.push('a exportação não gerou imagem');

  await browser.close();
  console.log(`capturas em ${out}`);
  console.log(errors.length ? errors.join('\n') : 'nenhum erro no console');
  process.exitCode = errors.length ? 1 : 0;
})();
