/*
 * Fetch the latest news for the frontpage
 */
async function update_frontpage_news(url) {
  let response = await fetch(url);
  let data = await response.json();

  let newsContainer = document.getElementById('newsContainer');

  data.forEach((n, i) => {
    if (i <= 5) {
      let article = document.createElement('div');
      article.className = 'newsWrapper';

      let anchor = document.createElement('a');
      anchor.name = '#' + n.id;
      article.appendChild(anchor);

      let title = document.createElement('div');
      title.className = 'newsTitle';
      title.innerText = n.title;
      article.appendChild(title);

      let date = document.createElement('div');
      date.className = 'newsDate';
      date.innerHTML = '<i class="fa fa-clock-o"></i> ' + n.datetime.split('T')[0] + ' by ' + n.authorname;
      article.appendChild(date);

      let newstext = document.createElement('div');
      newstext.className = 'newsText';
      newstext.innerHTML = n.summary;
      article.appendChild(newstext);

      newsContainer.appendChild(article);
    }
  });

  if (window.location.hash) {
    let el = document.querySelector('a[name="#' + window.location.hash.substring(1) + '"]');
    if (el) {
      el.scrollIntoView();
    }
  }
}
