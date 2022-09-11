<script lang="ts">
	/*
		TODO:
		- Read markers
		- Better post nav
		- Author/link/comment count
		- HN support
	*/

	import Comment from '$lib/Comment.svelte';
	import Post from '$lib/Post.svelte';

	import { onMount } from 'svelte';

	let redditData = null;

	onMount(async () => {
    fetchAndRedditData();
  });

	async function fetchAndRedditData() {
    const req = await fetch('http://localhost:8000');
		redditData = await req.json();
  }


</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<h1>Foobarbaz</h1>
	{#if redditData}
		<div>{redditData.time}</div>
		{#each Object.entries(redditData.subreddits) as [subreddit, subredditData]}
			<h2>{subreddit}</h2>

			{#each subredditData as post}
				<Post post={post} />
			{/each}
		{/each}
	{/if}
</section>

<style>
</style>
