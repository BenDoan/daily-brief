<script lang="ts">
	/*
		TODO:
		- Better post nav
		- Author/link/comment count
		- HN support
    - Show site
		- One post at a time
		- marker for op
	*/

	import Comment from '$lib/Comment.svelte';
	import Post from '$lib/Post.svelte';
	import { reset, currentTime } from '$lib/stores.js';

	import { onMount } from 'svelte';

	const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
	const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];


	let redditData = null;
	let time = null;

	onMount(async () => {
    fetchAndRedditData();
  });


	async function fetchAndRedditData() {
		const req = await fetch('/api/data');
		redditData = await req.json();
		const timeStr = redditData.time;
		time = new Date(timeStr);

		if (!$currentTime || timeStr > $currentTime) {
			reset();
			$currentTime = timeStr
		}
  }


</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	{#if time}
	<h1 title="{time.toLocaleString()}">{months[time.getMonth()]}, {days[time.getDay()]} {time.getDate()}</h1>
	{/if}
	{#if redditData}
		{#each Object.entries(redditData.subreddits) as [subreddit, subredditData]}
			<h3>{subreddit}</h3>

			{#each subredditData as post}
				<Post post={post} />
			{/each}
		{/each}
	{/if}
</section>

<style>
</style>
