<script lang="ts">
	import Comment from '$lib/Comment.svelte';
	import {marked} from 'marked';

	export let comment;
	const data = comment.data;

	const depth = data?.depth ?? 0;
	let is_open = true;

	const body = data.body;
	const body_html = marked.parse(body || "")

	function handleClick() {
		is_open = is_open ? false : true;
	}
</script>

<section class="depth-{depth}">
	<div>
		<div class="comment">
			<div class="meta">
				<span class="toggle" on:click={handleClick}>
					{#if is_open} [-] {:else} [+] {/if}
				</span>
				{data.author}
			</div>

			{#if is_open}
				<div class="body">{@html body_html}</div>
				{#if data?.replies}
					<div class="replies">
						{#each data.replies.data.children as reply}
							<Comment comment={reply} />
						{/each}
					</div>
				{/if}
			{/if}
		</div>
	</div>
</section>

<style>
.comment {
	margin-bottom: 2px;
	padding: 5px;
}

.body :global(p) {
	margin: 5px;
}

.toggle {
	cursor: pointer;
	user-select: none;
}

.meta {
	border-bottom: 1px solid black;
}

.depth-0 {
	margin-bottom: 10px;
	margin-left: 0;
	background-color: #fff;
}

.depth-1 {
	margin-left: 10px;
	background-color: #eee;
}

.depth-2 {
	margin-left: 20px;
	background-color: #ddd;
}

.depth-3 {
	margin-left: 30px;
	background-color: #ccc;
}

.depth-4 {
	margin-left: 40px;
	background-color: #fff;
}

.depth-5 {
	margin-left: 50px;
	background-color: #eee;
}

.depth-6 {
	margin-left: 60px;
	background-color: #ddd;
}

.depth-7 {
	margin-left: 70px;
	background-color: #ccc;
}

.depth-8 {
	margin-left: 80px;
	background-color: #fff;
}

.depth-9 {
	margin-left: 90px;
	background-color: #eee;
}

.depth-10 {
	margin-left: 100px;
	background-color: #ddd;
}
</style>

