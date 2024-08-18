<script>

	/** @type {import('./$types').PageData} */


	export let data;
	let script_data = data.vid_script_data;
	let vid_config_all = data.vid_config_all;
	let default_voice;

	async function updateScript() {
		if (default_voice!=null || default_voice!==undefined) {
			for(let i = 0; i < script_data.length; i++) {
				if(!(script_data[i].voice!=null && script_data[i].voice!==undefined)) {
					script_data[i].voice = default_voice;
				}
			}
		}
		const response = await fetch('http://127.0.0.1:4000/update_script/'+data.video_data.id, {
			method: 'PUT',
			body: JSON.stringify({ script_data, video_data: data.video_data }),
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
				<select bind:value={sd.voice}>
					<option value={null}>Default</option>
					/
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
			<select bind:value={data.video_data.background_video}>
				<option value={null}>Default</option>
				{#each Object.entries(vid_config_all.videos) as [video, vx]}
					<option value={video}>
						{video}
					</option>
				{/each}
			</select>
			Select a audio
			<select bind:value={data.video_data.background_music}>
				<option value={null}>Default</option>
				/
				{#each Object.entries(vid_config_all.audios) as [audios, vx]}
					<option value={audios}>
						{audios}
					</option>
				{/each}
			</select>
			Select default Voice
			<select bind:value={default_voice}>
				<option value=null>Default</option>
				{#each vid_config_all.voices as voice}
					<option value={voice.FriendlyName}>
						{voice.FriendlyName}{voice.Gender}
					</option>
				{/each}
			</select>
			Job Status
			<select bind:value={data.video_data.job_status}>
				<option value='Default'>Default</option>
				<option value='WIP'>WIP</option>
				<option value='Ready'>Ready</option>
			</select>
			<br />
			Video Orientation
			<select bind:value={data.video_data.v_or_h_or_b}>
				<option value='v'>Vertical</option>
				<option value='h'>Horizontal</option>
				<option value='b'>Both</option>
			</select>
			BG Volume<input type='number' bind:value={data.video_data.background_music_volume} step='0.01'>
			Text Color<input type="color" id="favcolor" bind:value={data.video_data.back_ground_col}>
			Border Color<input type="color" id="favcolor1" bind:value={data.video_data.border_col}>
			<button class='btn-primary' on:click={updateScript}>Save</button>
		</div>
	</div>
</div>