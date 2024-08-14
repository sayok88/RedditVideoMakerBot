<script>
	import MainEditor from '../story/MainEditor.svelte';

	let stories = [];
	let new_story;

	async function getNewStory() {
		if (new_story) {
			const res = await fetch(`http://127.0.0.1:4000/get_story/` + new_story);
			const item = await res.json();
			item.additional_end_text = 'Update';
			item.selected_comments = [];
			stories.push(item);
			stories = stories;
			new_story = null;
		}
	}
	async function createvidscript() {
		let data = {};
		for (let story of stories){
			data[story.thread_id] = story.selected_comments;
		}
		const response = await fetch('http://127.0.0.1:4000/create_multi_thread_script', {
			method: 'POST',
			body: JSON.stringify(data),
			headers: {
				'Content-Type': 'application/json'
			}
		});
	}

</script>
<style>
		  textarea {
        field-sizing: content;
    }

    .container {
        display: flex;
        flex-direction: row;
        max-width: 100%;
    }

    .item {
        box-sizing: border-box;
        max-width: 50%;
        display: inline-block;
        width: 100%;
    }
	</style>
<div class='container'>
	<div class='item'>
		<div class='text-column'>
			{#each stories as story}
				<MainEditor bind:data={story} showVideoEditor={false} bind:selected_comments={story.selected_comments} />
				<textarea placeholder='Additional End text' bind:value={story.additional_end_text}></textarea>
			{/each}
			<label>Fetch New Story</label>
			<input type='text' class='border-2' bind:value={new_story} placeholder='thread id like jkj2q3' />
			<button class='btn btn-primary' type='button' on:click={getNewStory}>Fetch</button>
		</div>
	</div>
	<div class='item'>
		<div class='text-column'>My script</div>
		{#each stories as story}
			{#each story.selected_comments as comment1}
				<div href='#'
						 class='block p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700'>
					<p class='font-normal text-gray-700 dark:text-gray-400'>{comment1.text}</p>
				</div>
			{/each}
		{/each}
		<button class='btn btn-primary btn-lg' type='button' on:click={createvidscript}>Post Script</button>
	</div>
</div>