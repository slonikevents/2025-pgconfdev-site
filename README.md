# PGConf.dev Static Site

This repository contains both the content of the PGConf.dev static site as well
as the tooling required to render it. All tasks are executed through [Invoke].

## Prerequisites

* Git ≥ 2.40
* Python ≥ 3.11

## Setup

1. Clone the repository and `cd` into it:

   ```bash
   git clone git@github.com:ktchen14/static-site.git
   cd static-site
   ```

2. If you have [direnv](https://direnv.net), then you just need to authorize the
   bundled `.envrc`:

   ```bash
   direnv allow
   ```

   Otherwise, create a virtualenv and activate it:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip3 install --upgrade pip
   ```

3. Install dependencies:

   ```bash
   pip3 install -r requirements.txt
   ```

4. Verify that [Invoke] is runnable by listing tasks with `invoke -l`. The
   output should resemble:

   ```
   Available tasks:

     render   Render the static site (into `site`)
     server   Open an HTTP server to serve the rendered site
   ```

## Rendering the Site

Use the `invoke render` command to render the site. The output should resemble:

```
Rendering 'contact.html.j2' to 'site/contact.html' ...
Copying 'static/logo/header.png' to 'site/static/logo/header.png' ...
...
Copying 'static/news.js' to 'site/static/news.js' ...
```

This command copies each file in the repository into its corresponding location
in the `site` subdirectory.

Any file ignored by Git, or having the `site-ignore` Git attribute, is skipped.
Files with the `.j2` extension are rendered using Jinja2 before being copied to
a destination file without the `.j2` extension.

## Viewing the Site

You can open rendered files in the `site` subdirectory directly in a browser to
view the site.

To ensure that the site looks as expected when it's served from an actual web
server, use the `invoke server` command to open an HTTP server that will serve
the `site` subdirectory.

## Publishing

Simply push to the `main` branch to publish the site. The "[Deploy to GitHub
Pages]" workflow in GitHub Actions listens for changes on this branch.

## Contributing

1. Keep it simple. This site should be updateable by nontechnical people.
   * Avoid Jinja2 control structures whenever possible. For example, rather
     than an `{% if ... %}` statement, just comment out the unused branch.

2. Write all prose in [Standard Canadian English]. In Vim, this is `set spell
   spelllang=en_ca`.

3. In general, follow the [Google HTML/CSS Style Guide], with the following
   exceptions:
   * Ignore [Rule 4.1.8 (Shorthand Properties)] in cases where only one value is
     explicitly set, as well as complex properties such as `background` and
     `font`.
   * Ignore [Rule 4.1.11 (Hexadecimal Notation)].
   * Ignore [Rule 4.2.6 (Selector and Declaration Separation)].
   * Ignore [Rule 4.2.7 (Rule Separation)] in rare cases.

4. Follow the Jinja2 style established in its [Template Designer Documentation].

5. Keep the site accessible.
   * Ensure that your changes render correctly on both smaller and larger
     screens.
   * Use `<div>`s and `<span>`s sparingly. Before you use one, ensure that you
     don't want a better [HTML element].

[Deploy to GitHub Pages]: https://github.com/ktchen14/static-site/actions/workflows/main.yaml
[Google HTML/CSS Style Guide]: https://google.github.io/styleguide/htmlcssguide.html
[HTML element]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element
[Invoke]: https://www.pyinvoke.org/
[Rule 4.1.11 (Hexadecimal Notation)]: https://google.github.io/styleguide/htmlcssguide.html#Hexadecimal_Notation
[Rule 4.1.8 (Shorthand Properties)]: https://google.github.io/styleguide/htmlcssguide.html#Shorthand_Properties
[Rule 4.2.6 (Selector and Declaration Separation)]: https://google.github.io/styleguide/htmlcssguide.html#Selector_and_Declaration_Separation
[Rule 4.2.7 (Rule Separation)]: https://google.github.io/styleguide/htmlcssguide.html#Rule_Separation
[Standard Canadian English]: https://en.wikipedia.org/wiki/Standard_Canadian_English
[Template Designer Documentation]: https://jinja.palletsprojects.com/en/3.1.x/templates/
