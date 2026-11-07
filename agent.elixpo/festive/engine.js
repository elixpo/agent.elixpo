/*
 * Elixpo festive themes. Generated into public/festive/theme.js by scripts/build-festive.mjs,
 * which inlines config/festivals.yaml as CALENDAR. Sites opt in with one script tag:
 *   <script src="https://agent.elixpo.com/festive/theme.js" defer></script>
 * The layer is decorative: it never blocks input and never restyles a site's own components.
 */
(function () {
  "use strict";
  var CALENDAR = /*__ELIXPO_FESTIVE_CALENDAR__*/ null;
  if (!CALENDAR || window.ElixpoFestive) return;

  var THEMES = {
    "diwali": { accent: "#f59e0b", colors: ["#ffb347", "#ff7a1a", "#ffd166", "#e85d04"], particle: "ember", garland: "lights" },
    "holi": { accent: "#ec4899", colors: ["#ff4d9d", "#4dabff", "#ffd23f", "#3ddc84", "#a259ff"], particle: "powder", garland: "bunting" },
    "independence-day": { accent: "#ff9933", colors: ["#ff9933", "#ffffff", "#138808", "#000080"], particle: "confetti", garland: "bunting" },
    "republic-day": { accent: "#138808", colors: ["#ff9933", "#ffffff", "#138808", "#000080"], particle: "confetti", garland: "bunting" },
    "durga-puja": { accent: "#d00000", colors: ["#d00000", "#ffba08", "#ffffff", "#f48c06"], particle: "petal", garland: "lights" },
    "christmas": { accent: "#c1121f", colors: ["#ffffff", "#e0f2fe", "#c1121f", "#2d6a4f"], particle: "snow", garland: "lights" },
    "new-year": { accent: "#eab308", colors: ["#ffd166", "#c7d2fe", "#ffffff", "#ff6b6b"], particle: "sparkle", garland: "lights" },
    "winter": { accent: "#60a5fa", colors: ["#ffffff", "#dbeafe", "#bfdbfe"], particle: "snow", garland: null },
    "summer": { accent: "#f59e0b", colors: ["#ffd166", "#ffb347", "#fde68a"], particle: "sun", garland: null }
  };

  var DAY = 86400000;
  var dayNumber = function (iso) { var p = iso.split("-").map(Number); return Date.UTC(p[0], p[1] - 1, p[2]) / DAY; };
  var todayIso = function () {
    try { return new Intl.DateTimeFormat("en-CA", { timeZone: CALENDAR.timezone, year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date()); }
    catch (e) { return new Date().toISOString().slice(0, 10); }
  };

  function occurrences(festival, year) {
    if (festival.every_year) return [year - 1, year, year + 1].map(function (y) { var iso = y + "-" + festival.every_year; return { start: iso, end: iso }; });
    return (festival.dates || []).map(function (d) { return { start: d.start, end: d.end || d.start }; });
  }

  function resolve(iso) {
    var today = dayNumber(iso), year = Number(iso.slice(0, 4)), best = null;
    CALENDAR.festivals.forEach(function (festival) {
      var before = festival.before != null ? festival.before : CALENDAR.defaults.before;
      var after = festival.after != null ? festival.after : CALENDAR.defaults.after;
      occurrences(festival, year).forEach(function (o) {
        var start = dayNumber(o.start), end = dayNumber(o.end);
        if (today < start - before || today > end + after) return;
        var distance = today < start ? start - today : today > end ? today - end : 0;
        if (!best || distance < best.distance) best = { festival: festival, distance: distance };
      });
    });
    if (best) return { id: best.festival.id, name: best.festival.name, greeting: best.festival.greeting, festival: true };
    var month = Number(iso.slice(5, 7));
    var season = (CALENDAR.seasons || []).filter(function (s) { return s.months.indexOf(month) !== -1; })[0];
    return season ? { id: season.id, name: season.name, greeting: null, festival: false } : null;
  }

  function pick() {
    var param = null;
    try { param = new URLSearchParams(location.search).get("festive"); } catch (e) { /* no URL API */ }
    if (param === "off" || CALENDAR.override === "none") return null;
    var forced = param || CALENDAR.override;
    if (forced && THEMES[forced]) {
      var known = CALENDAR.festivals.concat(CALENDAR.seasons || []).filter(function (f) { return f.id === forced; })[0] || {};
      return { id: forced, name: known.name || forced, greeting: known.greeting || null, festival: !!known.greeting };
    }
    var host = location.hostname.replace(/^www\./, "");
    var local = host === "localhost" || host === "127.0.0.1";
    if (!local && CALENDAR.services.indexOf(host) === -1) return null;
    return resolve(todayIso());
  }

  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) { /* storage unavailable */ } }
  };

  var CSS = [
    "#elixpo-festive{position:fixed;inset:0;z-index:9990;pointer-events:none;overflow:hidden;contain:strict}",
    "#elixpo-festive .ef-glow{position:absolute;inset:0 0 auto;height:42vh;background:radial-gradient(ellipse 60% 100% at 50% 0,var(--ef-accent-soft),transparent 70%)}",
    "#elixpo-festive .ef-garland{position:absolute;inset:0 0 auto;height:16px}",
    "#elixpo-festive .ef-garland.lights{background:radial-gradient(circle at 18px 7px,var(--ef-c0) 0 3px,transparent 4.5px) 0 0/72px 16px,radial-gradient(circle at 54px 7px,var(--ef-c1) 0 3px,transparent 4.5px) 0 0/72px 16px;filter:drop-shadow(0 0 4px var(--ef-c0))}",
    "#elixpo-festive .ef-garland.lights::after{content:'';position:absolute;inset:0;background:radial-gradient(circle at 36px 9px,var(--ef-c2) 0 3px,transparent 4.5px) 0 0/72px 16px;animation:ef-blink 1.8s ease-in-out infinite alternate}",
    "#elixpo-festive .ef-garland.bunting{height:18px;background:conic-gradient(from 135deg at 50% 0,var(--ef-c0) 0 90deg,transparent 0) 0 0/66px 18px,conic-gradient(from 135deg at 50% 0,var(--ef-c1) 0 90deg,transparent 0) 22px 0/66px 18px,conic-gradient(from 135deg at 50% 0,var(--ef-c2) 0 90deg,transparent 0) 44px 0/66px 18px}",
    "#elixpo-festive .ef-p{position:absolute;top:0;left:var(--x);width:var(--s);height:var(--s);background:var(--c);border-radius:50%;opacity:0;will-change:transform,opacity;animation:var(--anim) var(--d) linear var(--delay) infinite}",
    "#elixpo-festive .ef-ember{top:100%;box-shadow:0 0 10px 2px var(--c)}",
    "#elixpo-festive .ef-snow{top:-12px}",
    "#elixpo-festive .ef-confetti{top:-14px;border-radius:2px;height:calc(var(--s)*.45)}",
    "#elixpo-festive .ef-petal{top:-14px;border-radius:70% 0 70% 0}",
    "#elixpo-festive .ef-powder{top:100%;width:calc(var(--s)*4);height:calc(var(--s)*4);background:radial-gradient(circle,var(--c),transparent 68%)}",
    "#elixpo-festive .ef-sun{top:100%;width:calc(var(--s)*2.4);height:calc(var(--s)*2.4);background:radial-gradient(circle,var(--c),transparent 70%)}",
    "#elixpo-festive .ef-sparkle{top:var(--y);border-radius:0;clip-path:polygon(50% 0,61% 39%,100% 50%,61% 61%,50% 100%,39% 61%,0 50%,39% 39%)}",
    "@keyframes ef-rise{0%{transform:translate3d(0,0,0);opacity:0}10%{opacity:.75}80%{opacity:.5}100%{transform:translate3d(var(--drift),-108vh,0);opacity:0}}",
    "@keyframes ef-fall{0%{transform:translate3d(0,0,0) rotate(0);opacity:0}8%{opacity:.8}90%{opacity:.65}100%{transform:translate3d(var(--drift),108vh,0) rotate(var(--spin));opacity:0}}",
    "@keyframes ef-twinkle{0%,100%{transform:scale(.3);opacity:0}50%{transform:scale(1.2) rotate(45deg);opacity:.85}}",
    "@keyframes ef-blink{from{opacity:.25}to{opacity:1}}",
    ".ef-badge{position:fixed;left:16px;bottom:16px;z-index:9991;display:flex;align-items:center;gap:10px;max-width:calc(100vw - 32px);padding:8px 10px 8px 14px;border-radius:999px;background:rgba(20,20,20,.86);color:#fff;font:600 12px/1.2 system-ui,-apple-system,'Segoe UI',sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.25),inset 0 0 0 1px var(--ef-accent);animation:ef-in .5s cubic-bezier(.3,1.4,.5,1)}",
    ".ef-badge b{color:var(--ef-accent)}",
    ".ef-badge button{width:22px;height:22px;flex:none;border:0;border-radius:50%;background:rgba(255,255,255,.14);color:#fff;font:700 14px/1 system-ui;cursor:pointer}",
    ".ef-badge button:hover{background:var(--ef-accent)}",
    "@keyframes ef-in{from{transform:translateY(16px);opacity:0}to{transform:none;opacity:1}}",
    "html[data-elixpo-festive] ::selection{background:var(--ef-accent-soft-strong)}",
    "@media (prefers-reduced-motion:reduce){#elixpo-festive .ef-p{display:none}#elixpo-festive .ef-garland::after,.ef-badge{animation:none}}",
    "@media print{#elixpo-festive,.ef-badge{display:none}}"
  ].join("");

  var PARTICLES = {
    ember: { anim: "ef-rise", dur: [9, 15] },
    powder: { anim: "ef-rise", dur: [12, 20] },
    sun: { anim: "ef-rise", dur: [16, 26] },
    snow: { anim: "ef-fall", dur: [10, 18] },
    confetti: { anim: "ef-fall", dur: [7, 12] },
    petal: { anim: "ef-fall", dur: [9, 15] },
    sparkle: { anim: "ef-twinkle", dur: [2.4, 4.2] }
  };

  var hexAlpha = function (hex, a) { var n = parseInt(hex.slice(1), 16); return "rgba(" + (n >> 16) + "," + ((n >> 8) & 255) + "," + (n & 255) + "," + a + ")"; };
  var rand = function (min, max) { return min + Math.random() * (max - min); };

  function mount(active) {
    var theme = THEMES[active.id];
    var root = document.documentElement;
    var dismissKey = "elixpo-festive-dismissed:" + active.id + ":" + todayIso().slice(0, 4);
    var dismissed = store.get(dismissKey) === "1";
    root.setAttribute("data-elixpo-festive", active.id);
    root.style.setProperty("--ef-accent", theme.accent);
    root.style.setProperty("--ef-accent-soft", hexAlpha(theme.accent, 0.12));
    root.style.setProperty("--ef-accent-soft-strong", hexAlpha(theme.accent, 0.32));
    theme.colors.slice(0, 3).forEach(function (c, i) { root.style.setProperty("--ef-c" + i, c); });

    var style = document.createElement("style");
    style.id = "elixpo-festive-style";
    style.textContent = CSS;
    document.head.appendChild(style);

    var layer = document.createElement("div");
    layer.id = "elixpo-festive";
    layer.setAttribute("aria-hidden", "true");
    layer.innerHTML = '<div class="ef-glow"></div>' + (theme.garland ? '<div class="ef-garland ' + theme.garland + '"></div>' : "");
    if (!dismissed) {
      var kind = PARTICLES[theme.particle];
      var count = window.matchMedia("(max-width: 640px)").matches ? 7 : 14;
      for (var i = 0; i < count; i++) {
        var p = document.createElement("i");
        p.className = "ef-p ef-" + theme.particle;
        var props = {
          "--x": rand(0, 100).toFixed(1) + "vw", "--y": rand(8, 85).toFixed(1) + "vh",
          "--s": rand(5, 11).toFixed(1) + "px", "--c": theme.colors[i % theme.colors.length],
          "--d": rand(kind.dur[0], kind.dur[1]).toFixed(1) + "s", "--delay": (-rand(0, kind.dur[1])).toFixed(1) + "s",
          "--drift": rand(-60, 60).toFixed(0) + "px", "--spin": rand(-540, 540).toFixed(0) + "deg", "--anim": kind.anim
        };
        for (var key in props) p.style.setProperty(key, props[key]);
        layer.appendChild(p);
      }
    }
    document.body.appendChild(layer);

    if (active.festival && active.greeting && !dismissed) {
      var badge = document.createElement("div");
      badge.className = "ef-badge";
      badge.setAttribute("role", "note");
      badge.innerHTML = "<span><b>✦</b> " + active.greeting + " from Elixpo</span>";
      var close = document.createElement("button");
      close.type = "button";
      close.setAttribute("aria-label", "Hide the " + active.name + " greeting and effects");
      close.textContent = "×";
      close.addEventListener("click", function () {
        store.set(dismissKey, "1");
        badge.remove();
        layer.querySelectorAll(".ef-p").forEach(function (p) { p.remove(); });
      });
      badge.appendChild(close);
      document.body.appendChild(badge);
    }
  }

  var active = pick();
  window.ElixpoFestive = { active: active, calendar: CALENDAR, resolve: resolve };
  if (!active || !THEMES[active.id]) return;
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { mount(active); });
  else mount(active);
})();
