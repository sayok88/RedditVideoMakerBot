<script>
	export let per_page, total_items, total_pages, next_page, current_page;
	export let page_click = (x) => {
		console.log(x);
	};

	function page_click2(pg) {
		console.log(pg);
		page_click(pg);
	}
</script>
<style>
    .pagination {
        display: inline-block;
    }

    .pagination button {
        color: black;
        float: left;
        padding: 8px 16px;
        text-decoration: none;
    }
</style>
<div class='container'>
	<div class='pagination'>
		{#if current_page > 1}
			<button on:click={()=>page_click2(current_page-1)}>&laquo;</button>
		{/if}
		{#each { length: total_pages } as _, i}
			{#if current_page == i + 1 }
				<button class='bg-gray-800 ' style='color: white'>{i + 1}</button>
			{:else }
				<button on:click={()=>page_click2(i+1)}>{i + 1}</button>
			{/if}
		{/each}
		{#if current_page < total_pages}
			<button on:click={()=>page_click2(next_page)}>&raquo;</button>
		{/if}
	</div>
</div>