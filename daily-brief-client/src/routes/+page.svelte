<script lang="ts">
	/*
		TODO:
		- Better post nav
		- Author/link/comment count
		- HN support
    - Show site
		- One post at a time
		- marker for op
		- news
		- weather
		- better mobile support
	*/

	import Comment from '$lib/Comment.svelte';
	import Post from '$lib/Post.svelte';
	import { reset, currentTime } from '$lib/stores.js';
	import favicon from '$lib/assets/favicon.ico';


	import { dev } from '$app/environment';
	import { onMount } from 'svelte';

	const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
	const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];


	let redditData = null;
	let time = null;
	let hasNyt = false;

	const nytUrl = dev ? 'http://localhost:8000/img/nyt.pdf' : '/img/nyt.pdf'

	onMount(async () => {
    fetchAndSetRedditData();
		fetchNyt();
  });


	async function fetchAndSetRedditData() {
		const url = dev ? 'http://localhost:8000/api/data' : '/api/data'
		const req = await fetch(url, {
			headers: {
				'Authorization': 'Basic Og=='
			}
		});
		redditData = await req.json();
		const timeStr = redditData.time;
		time = new Date(timeStr);

		if (!$currentTime || timeStr > $currentTime) {
			reset();
			$currentTime = timeStr
		}
  }

	async function fetchNyt() {
		const req = await fetch(nytUrl, {
			headers: {
				'Authorization': 'Basic Og=='
			}
		});
		hasNyt = req.status === 200
  }


</script>

<svelte:head>
	<title>Daily Brief</title>
	<link rel="icon" href={favicon} />

</svelte:head>

<section>
	{#if time}
		<h1 class="title">Daily Brief</h1>
		<h3 class="subtitle" title="{time.toLocaleString()}">{days[time.getDay()]}, {months[time.getMonth()]} {time.getDate()} {time.getFullYear()}</h3>
	{/if}

	{#if hasNyt}
		<iframe src="{nytUrl}#zoom=100&toolbar=0" width="100%" height="2150px" frameborder="0" scrolling="no" />
	{/if}

	{#if redditData}
		{#each Object.entries(redditData.subreddits) as [subreddit, subredditData]}
			<h3>/r/{subreddit}</h3>

			{#each subredditData as post}
				<Post post={post} />
			{/each}
		{/each}
	{/if}

</section>

<style>
.title {
	font-family: serif;
	text-align: center;
	font-size: 40pt;
	margin-top: 5px;
	margin-bottom: 5px;
	font-weight: 1000;
}

.subtitle {
	font-size: 12pt;
	font-family: serif;
	text-align: center;
	margin-top: 5px;
	margin-bottom: 5px;
}
</style>
