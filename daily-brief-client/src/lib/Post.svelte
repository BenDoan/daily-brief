<script lang="ts">
	import Comment from '$lib/Comment.svelte';
	import {marked} from 'marked';

	export let post;

	let is_open = false;

	const url = post[0].data.children[0].data.url;

	const selftext = post[0].data.children[0].data.selftext;
	const selftext_html = marked.parse(selftext)

	const is_img = url.includes(".jpg") || url.includes(".png") || url.includes("jpeg")
	console.log(post)


	function handleClick() {
		is_open = is_open ? false : true;
	}
</script>

<div class="comments">
	<h3>
		<span class="toggle" on:click={handleClick}>
			{#if is_open} [-] {:else} [+] {/if}
		</span>
		{post[0].data.children[0].data.title}
		{#if is_img}[i]{/if}
	</h3>
	{#if is_open}
		{#if is_img}
			<img class="img" src="{url}" />
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
	max-width:70vw;
}

pre {
	white-space: pre-wrap
}
</style>

