(function () {
  const ALL_MODULES = "all";

  function baseName(path) {
    return decodeURIComponent((path || "").split("/").pop() || "index.html");
  }

  function rootPrefix() {
    const parts = decodeURIComponent(window.location.pathname || "").split("/");
    return parts.length >= 2 && parts[parts.length - 2] === "html" ? "../" : "";
  }

  function siteHref(href) {
    if (!href || /^(https?:|mailto:|#)/.test(href)) return href;
    return `${rootPrefix()}${href}`;
  }

  function moduleById(manifest, id) {
    return (manifest.modules || []).find((module) => module.id === id) || null;
  }

  function pagesInModule(manifest, id) {
    return (manifest.pages || []).filter((page) => page.module === id && page.status !== "defer");
  }

  function publishablePages(manifest) {
    return (manifest.pages || []).filter((page) => page.status !== "defer");
  }

  function groupPages(pages) {
    const groups = [];
    pages.forEach((page) => {
      const title = page.group || "Other";
      let group = groups.find((candidate) => candidate.title === title);
      if (!group) {
        group = { title, pages: [] };
        groups.push(group);
      }
      group.pages.push(page);
    });
    return groups;
  }

  function makeLink(href, label) {
    const link = document.createElement("a");
    link.href = siteHref(href);
    link.textContent = label;
    return link;
  }

  function collectionAuthors(collection) {
    const authors = collection.authors || [];
    if (!authors.length) return collection.author || "";
    return authors.map((author) => {
      const details = [author.role, author.affiliation].filter(Boolean).join(", ");
      return details ? `${author.name} (${details})` : author.name;
    }).filter(Boolean).join("; ");
  }

  function pageByFilename(manifest, filename) {
    return publishablePages(manifest).find((page) => page.filename === filename || page.filename.endsWith(`/${filename}`)) || null;
  }

  function pageSearchText(manifest, page) {
    const moduleInfo = moduleById(manifest, page.module);
    return [
      page.title,
      page.group,
      page.learning_goal,
      page.prereqs,
      page.filename,
      moduleInfo && moduleInfo.title,
    ].filter(Boolean).join(" ").toLowerCase();
  }

  function createPageCard(page, options = {}) {
    const card = document.createElement("article");
    card.className = "phys681-card phys681-viz-card";
    card.dataset.module = page.module;
    card.dataset.group = page.group || "";
    card.dataset.search = options.searchText || "";

    const preview = document.createElement("div");
    preview.className = "phys681-card-preview";
    if (page.screenshot) {
      const image = document.createElement("img");
      image.src = siteHref(page.screenshot);
      image.alt = "";
      preview.append(image);
    } else {
      const label = document.createElement("span");
      label.className = "phys681-card-preview-label";
      label.textContent = page.group || "Visualization";
      preview.append(label);
    }

    const body = document.createElement("div");
    body.className = "phys681-card-body";
    const heading = document.createElement(options.headingLevel || "h3");
    heading.textContent = page.title;

    const goal = document.createElement("p");
    goal.textContent = page.learning_goal;

    const meta = document.createElement("div");
    meta.className = "phys681-card-meta";
    [
      page.group,
      page.tier === "A" ? "Core" : "Supplemental",
      `${page.expected_minutes} min`,
    ].filter(Boolean).forEach((label) => {
      const chip = document.createElement("span");
      chip.className = "phys681-chip";
      chip.textContent = label;
      meta.append(chip);
    });
    if (page.prereqs) {
      const prereq = document.createElement("span");
      prereq.className = "phys681-chip phys681-chip-muted";
      prereq.textContent = `Assumes: ${page.prereqs}`;
      meta.append(prereq);
    }

    body.append(heading, goal, meta);

    const actions = document.createElement("div");
    actions.className = "phys681-card-actions";
    actions.append(makeLink(page.filename, page.filename.endsWith("narratives.html") ? "Read notes" : "Launch"));
    if (page.narrative_anchor && page.narrative_anchor !== "#") actions.append(makeLink(page.narrative_anchor, "Context in notes"));

    card.append(preview, body, actions);
    return card;
  }

  function createTopicSection(title, pages, manifest) {
    const section = document.createElement("section");
    section.className = "phys681-topic-section";

    const heading = document.createElement("div");
    heading.className = "phys681-section-heading";
    const h2 = document.createElement("h2");
    h2.textContent = title;
    const count = document.createElement("span");
    count.textContent = `${pages.length} ${pages.length === 1 ? "item" : "items"}`;
    heading.append(h2, count);

    const grid = document.createElement("div");
    grid.className = "phys681-grid phys681-viz-grid";
    pages.forEach((page) => {
      grid.append(createPageCard(page, {
        searchText: pageSearchText(manifest, page),
        headingLevel: "h3",
      }));
    });

    section.append(heading, grid);
    return section;
  }

  function injectNav(manifest) {
    const currentFile = baseName(window.location.pathname);
    const page = pageByFilename(manifest, currentFile);
    const collection = manifest.collection || {};
    const moduleInfo = page ? moduleById(manifest, page.module) : null;

    const navRoot = document.getElementById("site-nav-root");
    if (navRoot) {
      const bar = document.createElement("nav");
      bar.className = "phys681-sitebar";
      bar.setAttribute("aria-label", "Phys 681 teaching site navigation");

      const title = document.createElement("div");
      title.className = "phys681-site-title";

      const kicker = document.createElement("div");
      kicker.className = "phys681-site-kicker";
      kicker.textContent = moduleInfo ? moduleInfo.title : collection.title || "Phys 681";

      const current = document.createElement("div");
      current.className = "phys681-site-current";
      current.textContent = page ? page.title : document.title || "Teaching visualization";

      title.append(kicker, current);

      const links = document.createElement("div");
      links.className = "phys681-site-links";
      links.append(
        makeLink("index.html", "Home"),
        makeLink("html/module-emission-propagation.html", "Emission"),
        makeLink("html/module-interferometry-instrumentation.html", "Interferometry")
      );
      if (page && page.narrative_anchor) {
        links.append(makeLink(page.narrative_anchor, "Narrative"));
      }

      bar.append(title, links);
      navRoot.replaceChildren(bar);
    }

    const footerRoot = document.getElementById("site-footer-root");
    if (footerRoot) {
      const footer = document.createElement("footer");
      footer.className = "phys681-site-footer";

      const version = document.createElement("div");
      const authors = collectionAuthors(collection);
      version.innerHTML = `<strong>${collection.course || "Phys 681"}</strong> Teaching Collection ${collection.version || ""} &middot; ${collection.date || ""}${authors ? `<br>Authors: ${authors}` : ""}`;

      const footerLinks = document.createElement("div");
      footerLinks.className = "phys681-footer-links";

      if (page && moduleInfo) {
        const modulePages = pagesInModule(manifest, page.module);
        const index = modulePages.findIndex((candidate) => candidate.filename === page.filename);
        if (index > 0) footerLinks.append(makeLink(modulePages[index - 1].filename, "Previous"));
        if (index < modulePages.length - 1) footerLinks.append(makeLink(modulePages[index + 1].filename, "Next"));
      }

      if (collection.doi_url) footerLinks.append(makeLink(collection.doi_url, "Collection DOI"));
      if (collection.version_doi_url) footerLinks.append(makeLink(collection.version_doi_url, "This version"));
      footer.append(version, footerLinks);
      footerRoot.replaceChildren(footer);
    }

    if (page) {
      const navRoot = document.getElementById("site-nav-root");
      const next = navRoot && navRoot.nextElementSibling;
      const shouldAddBanner = next && !next.classList.contains("phys681-page-title") && !document.body.classList.contains("phys681-page");
      if (shouldAddBanner) {
        const banner = document.createElement("header");
        banner.className = "phys681-page-title";

        const moduleLabel = document.createElement("div");
        moduleLabel.className = "phys681-site-kicker";
        moduleLabel.textContent = [moduleInfo && moduleInfo.title, page.group].filter(Boolean).join(" · ");

        const title = document.createElement("h1");
        title.textContent = page.title;

        const goal = document.createElement("p");
        goal.textContent = page.learning_goal;

        banner.append(moduleLabel, title, goal);
        navRoot.insertAdjacentElement("afterend", banner);
      }
    }
  }

  function injectModuleCards(manifest) {
    document.querySelectorAll("[data-site-module]").forEach((container) => {
      const moduleId = container.getAttribute("data-site-module");
      const pages = pagesInModule(manifest, moduleId);
      const sections = groupPages(pages).map((group) => createTopicSection(group.title, group.pages, manifest));
      container.classList.add("phys681-topic-list");
      container.replaceChildren(...sections);
    });
  }

  function injectCatalog(manifest) {
    const catalog = document.querySelector("[data-site-index]");
    if (!catalog) return;

    let activeModule = ALL_MODULES;
    const search = document.getElementById("site-search");
    const filters = document.querySelector("[data-site-filters]");
    const pages = publishablePages(manifest);

    if (filters) {
      const filterItems = [
        { id: ALL_MODULES, title: "All" },
        ...(manifest.modules || []),
      ];
      filters.replaceChildren(...filterItems.map((moduleInfo) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "phys681-filter";
        button.dataset.moduleFilter = moduleInfo.id;
        button.textContent = moduleInfo.title;
        button.setAttribute("aria-pressed", moduleInfo.id === activeModule ? "true" : "false");
        button.addEventListener("click", () => {
          activeModule = moduleInfo.id;
          render();
        });
        return button;
      }));
    }

    function matchingPages() {
      const query = (search && search.value || "").trim().toLowerCase();
      return pages.filter((page) => {
        const inModule = activeModule === ALL_MODULES || page.module === activeModule;
        const matchesQuery = !query || pageSearchText(manifest, page).includes(query);
        return inModule && matchesQuery;
      });
    }

    function render() {
      if (filters) {
        filters.querySelectorAll("[data-module-filter]").forEach((button) => {
          button.setAttribute("aria-pressed", button.dataset.moduleFilter === activeModule ? "true" : "false");
        });
      }

      const visible = matchingPages();
      const byModule = [];
      (manifest.modules || []).forEach((moduleInfo) => {
        const modulePages = visible.filter((page) => page.module === moduleInfo.id);
        if (modulePages.length) byModule.push({ moduleInfo, pages: modulePages });
      });

      const nodes = byModule.flatMap(({ moduleInfo, pages: modulePages }) => {
        const moduleSection = document.createElement("section");
        moduleSection.className = "phys681-module-section";

        const heading = document.createElement("div");
        heading.className = "phys681-module-heading";
        const title = document.createElement("h2");
        title.textContent = moduleInfo.title;
        const description = document.createElement("p");
        description.textContent = moduleInfo.description;
        heading.append(title, description);

        const topicList = document.createElement("div");
        topicList.className = "phys681-topic-list";
        groupPages(modulePages).forEach((group) => {
          topicList.append(createTopicSection(group.title, group.pages, manifest));
        });

        moduleSection.append(heading, topicList);
        return [moduleSection];
      });

      if (!nodes.length) {
        const empty = document.createElement("p");
        empty.className = "phys681-empty";
        empty.textContent = "No visualizations match the current search.";
        nodes.push(empty);
      }

      catalog.replaceChildren(...nodes);
    }

    if (search) search.addEventListener("input", render);
    render();
  }

  function start() {
    const manifest = window.PHYS681_SITE_MANIFEST;
    if (!manifest) return;
    injectNav(manifest);
    injectModuleCards(manifest);
    injectCatalog(manifest);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
