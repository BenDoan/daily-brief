<script lang="ts">
	import Comment from '$lib/Comment.svelte';
	import {marked} from 'marked';
	import { seenPosts } from '$lib/stores.js';

	export let post;

	let is_open = false;

	const data = post[0].data.children[0].data;
	console.log(data);
	const url = data.url;
	const id = data.id;

	const selftext = data.selftext;
	const selftext_html = marked.parse(selftext || "")

	const is_img = url.includes(".jpg") || url.includes(".png") || url.includes("jpeg")

	function handleToggle() {
		is_open = is_open ? false : true;
		$seenPosts[id] = true;
	}
</script>

<div class="comments">
	<h3 class:seen={$seenPosts[id]}>
		<span class="toggle" on:click={handleToggle}>
			{#if is_open} [-] {:else} [+] {/if}
		</span>
		{#if data.url && !is_img && !selftext}
			<a href="{url}">{data.title}</a>
		{:else}
			{data.title}
		{/if}
		{#if is_img}[i]{/if}
</h3>
	{#if is_open}
		<div class="meta">
				&#11014;{data.score} - {data.author}
		</div>
		{#if is_img}
			<a href="{url}">
				<img class="img" src="{url}" />
			</a>
		{:else}
			{@html selftext_html}
		{/if}
		{#each post[1].data.children as commentData}
			<Comment comment={commentData} />
		{/each}
	{/if}
</div>

<style>
.toggle {
	cursor: pointer;
	user-select: none;
}

.img {
	max-width: 70vw;
	max-height: 70vh;
}

.meta {
	border: 1px solid #ddd;
	padding: 5px;
	margin-bottom: 5px;
}

.seen {
	color: #a3d;
}

.seen a:link {
	color: #a3d;
}
</style>

