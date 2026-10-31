/* OxidePM site behaviour: theme, menus, copy buttons, adapter workflow, adapter search, docs filter. */
(function () {
  "use strict";

  var doc = document;
  var root = doc.documentElement;

  function $(sel, ctx) { return (ctx || doc).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }

  /* ---- theme ---- */
  function themeNow() { return root.getAttribute("data-theme") === "dark" ? "dark" : "light"; }
  function syncThemeLabels() {
    var dark = themeNow() === "dark";
    var label = dark ? "Switch to light theme" : "Switch to dark theme";
    $$("[data-theme-toggle]").forEach(function (b) {
      b.setAttribute("aria-label", label);
      b.setAttribute("title", label);
    });
  }
  $$("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", function () {
      var next = themeNow() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("oxidepm-theme", next); } catch (e) {}
      syncThemeLabels();
    });
  });
  syncThemeLabels();

  /* ---- header menu (below 760px) ---- */
  var menuBtn = $("[data-menu-toggle]");
  var menu = $("#site-menu");
  if (menuBtn && menu) {
    var setMenu = function (open) {
      menu.hidden = !open;
      menuBtn.setAttribute("aria-expanded", String(open));
      menuBtn.textContent = open ? "Close" : "Menu";
    };
    menuBtn.addEventListener("click", function () { setMenu(menu.hidden); });
    if (window.matchMedia) {
      var mqMenu = window.matchMedia("(min-width: 760px)");
      var onMenuMq = function () { if (mqMenu.matches) setMenu(false); };
      if (mqMenu.addEventListener) mqMenu.addEventListener("change", onMenuMq);
    }
  }

  /* ---- copy buttons ---- */
  var copyStatus = $("#copy-status");
  var copyTimers = [];
  function legacyCopy(text) {
    var ta = doc.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    doc.body.appendChild(ta);
    ta.select();
    try { doc.execCommand("copy"); } catch (e) {}
    doc.body.removeChild(ta);
  }
  $$("[data-copy]").forEach(function (btn, i) {
    var label = btn.querySelector("[data-copy-label]");
    var idle = label ? label.textContent : btn.textContent;
    var done = function () {
      if (label) label.textContent = "Copied"; else btn.textContent = "Copied";
      if (copyStatus) copyStatus.textContent = btn.getAttribute("data-copy-message") || "Copied to clipboard";
      clearTimeout(copyTimers[i]);
      copyTimers[i] = setTimeout(function () {
        if (label) label.textContent = idle; else btn.textContent = idle;
        if (copyStatus) copyStatus.textContent = "";
      }, 1800);
    };
    btn.addEventListener("click", function () {
      var target = doc.getElementById(btn.getAttribute("data-copy"));
      var text = target ? target.textContent.replace(/\n$/, "") : "";
      var fallback = function () { legacyCopy(text); done(); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, fallback);
      else fallback();
    });
  });

  /* ---- home: the three-step adapter workflow ---- */
  var flow = $("[data-flow]");
  if (flow) {
    var stepBtns = $$("[data-step]", flow);
    var panels = $$("[data-panel]", flow);
    var stepLabel = $("[data-step-label]", flow);
    var consent = null; // null | "y" | "n"
    var showConsent = function () {
      $$("[data-pending]", flow).forEach(function (e) { e.hidden = consent !== null; });
      $$("[data-yes]", flow).forEach(function (e) { e.hidden = consent !== "y"; });
      $$("[data-no]", flow).forEach(function (e) { e.hidden = consent !== "n"; });
      $$("[data-done]", flow).forEach(function (e) { e.hidden = consent === null; });
    };
    var select = function (n) {
      stepBtns.forEach(function (b) { b.setAttribute("aria-pressed", String(+b.getAttribute("data-step") === n)); });
      panels.forEach(function (p) { p.hidden = +p.getAttribute("data-panel") !== n; });
      if (stepLabel) stepLabel.textContent = "step " + (n + 1) + " of 3";
      if (n !== 2) { consent = null; showConsent(); }
    };
    stepBtns.forEach(function (b) { b.addEventListener("click", function () { select(+b.getAttribute("data-step")); }); });
    $("[data-allow]", flow).addEventListener("click", function () { consent = "y"; showConsent(); });
    $("[data-deny]", flow).addEventListener("click", function () { consent = "n"; showConsent(); });
    $("[data-reset]", flow).addEventListener("click", function () { consent = null; showConsent(); });
    select(0);
  }

  /* ---- adapters: search and filter ---- */
  var ad = $("[data-adapters]");
  if (ad) {
    var input = $("[data-search]", ad);
    var radios = $$("input[name=adapter-filter]", ad);
    var cards = $$("[data-card]", ad);
    var grid = $("[data-grid]", ad);
    var empty = $("[data-empty]", ad);
    var resultText = $("[data-result]", ad);
    var queryText = $("[data-query]", ad);
    var filterNow = function () {
      var r = radios.filter(function (x) { return x.checked; })[0];
      return r ? r.value : "all";
    };
    var update = function () {
      var q = input.value.trim().toLowerCase();
      var f = filterNow();
      var counts = { all: 0, available: 0, later: 0 };
      var shown = 0;
      cards.forEach(function (c) {
        var match = !q || c.getAttribute("data-text").indexOf(q) !== -1;
        var status = c.getAttribute("data-status");
        if (match) { counts.all++; counts[status]++; }
        var visible = match && (f === "all" || f === status);
        c.hidden = !visible;
        if (visible) shown++;
      });
      ["all", "available", "later"].forEach(function (k) {
        var el = $("[data-count=" + k + "]", ad);
        if (el) el.textContent = String(counts[k]);
      });
      resultText.textContent = shown === 1 ? "1 adapter" : shown + " adapters";
      grid.hidden = shown === 0;
      empty.hidden = shown !== 0;
      queryText.textContent = input.value.trim();
    };
    input.addEventListener("input", update);
    radios.forEach(function (r) { r.addEventListener("change", update); });
    $("[data-clear]", ad).addEventListener("click", function () {
      input.value = "";
      radios.forEach(function (r) { r.checked = r.value === "all"; });
      update();
      input.focus();
    });
    update();
  }

  /* ---- docs: sidebar filter and mobile menu ---- */
  var filters = $$("[data-docs-filter]");
  if (filters.length) {
    var applyFilter = function (value, source) {
      var q = value.trim().toLowerCase();
      filters.forEach(function (f) { if (f !== source) f.value = value; });
      $$("[data-docs-nav]").forEach(function (nav) {
        var any = false;
        $$("[data-group]", nav).forEach(function (g) {
          var title = g.getAttribute("data-group").toLowerCase();
          var groupHit = false;
          $$("li", g).forEach(function (li) {
            var hit = !q || title.indexOf(q) !== -1 || li.textContent.toLowerCase().indexOf(q) !== -1;
            li.hidden = !hit;
            if (hit) groupHit = true;
          });
          g.hidden = !groupHit;
          if (groupHit) any = true;
        });
        var none = $("[data-docs-none]", nav);
        if (none) { none.hidden = any; $("[data-docs-query]", none).textContent = value.trim(); }
      });
    };
    filters.forEach(function (f) { f.addEventListener("input", function () { applyFilter(f.value, f); }); });
  }
  var docsToggle = $("[data-docs-toggle]");
  if (docsToggle) {
    var docsNav = $("#docs-nav");
    docsToggle.addEventListener("click", function () {
      var open = docsNav.hidden;
      docsNav.hidden = !open;
      docsToggle.setAttribute("aria-expanded", String(open));
      $("[data-docs-toggle-label]", docsToggle).textContent = open ? "Close" : "Menu";
    });
  }

  /* ---- 404: show the address that was asked for ---- */
  $$("[data-path]").forEach(function (el) {
    var p = window.location.pathname;
    if (p && !/404/.test(p)) el.textContent = p;
  });
})();
