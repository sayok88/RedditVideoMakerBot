import { dev } from '$app/environment';

// we don't need any JS on this page, though we'll load
// it in dev so that we get hot module replacement
export const csr = dev;

// since there's no dynamic data here, we can prerender
// it so that it gets served as a static asset in production
export const prerender = true;

/** @type {import('./$types').PageLoad} */
export async function load({ fetch, params }) {
	const res1 = await fetch(`http://127.0.0.1:4000/get_scripts/` + params.video_id);
	const item1 = await res1.json();
	const res2 = await fetch(`http://127.0.0.1:4000/video_config_all`);
	const item2 = await res2.json();

	return { vid_script_data: item1.response.script, vid_config_all: item2, video_data:item1.response.video };
}