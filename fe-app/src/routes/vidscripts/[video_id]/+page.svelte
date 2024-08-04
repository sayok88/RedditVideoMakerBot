<script>

	/** @type {import('./$types').PageData} */


	export let data;
	let script_data = data.vid_script_data;
	let vid_config_all = data.vid_config_all;
	let selected_video, selected_audio, default_voice;
</script>
<style>
    textarea {
        field-sizing: content;
    }

    .item {
        box-sizing: border-box;
        max-width: 70%;
        display: inline-block;
        width: 100%;
    }

    .container {
        display: flex;
        flex-direction: row;
        max-width: 100%;
    }
</style>
<svelte:head>
	<title>Home</title>
	<meta name='description' content='Video Script' />
</svelte:head>
<div class='container'>
	<div class='item'>
		<div class='text-column'>
			{#each script_data as sd}
				<textarea bind:value={sd.text}></textarea>
				select a voice
				<select bind:value={sd.selected_voice}>
					<option value='Default'>Default</option>/
					{#each vid_config_all.voices as voice}
						<option value={voice.FriendlyName}>
							{voice.FriendlyName}{voice.Gender}
						</option>
					{/each}
				</select>
			{/each}
		</div>
	</div>
	<div class='item'>
		<div class='text-column'>
			Select a video
			<select bind:value={selected_video}>
				{#each Object.entries(vid_config_all.videos) as [video, vx]}
					<option value={video}>
						{video}
					</option>
				{/each}
			</select>
			Select a audio
			<select bind:value={selected_audio}>
				{#each Object.entries(vid_config_all.audios) as [audios, vx]}
					<option value={audios}>
						{audios}
					</option>
				{/each}
			</select>
			Select default Voice
			<select bind:value={default_voice}>
					<option value='Default'>Default</option>/
					{#each vid_config_all.voices as voice}
						<option value={voice.FriendlyName}>
							{voice.FriendlyName}{voice.Gender}
						</option>
					{/each}
				</select>
		</div>
	</div>
</div>