<script lang="ts">
	import type { Application, AIProvider } from '$lib/types';

	interface Props {
		aiProvider: AIProvider;
		applications: Application[];
	}

	let { aiProvider, applications }: Props = $props();
</script>

<div class="relative rounded-2xl border border-white/25 backdrop-blur-sm bg-white/5 p-6 min-w-[480px] max-w-2xl">
	<!-- AI Provider Header -->
	<div class="flex items-center gap-3 mb-6">
		<img src={aiProvider.icon} alt={aiProvider.name} class="w-8 h-8 object-contain" />
		<h2 class="text-xl font-semibold text-white">{aiProvider.name}</h2>
	</div>

	<!-- Applications Table -->
	<div class="overflow-x-auto">
		<table class="w-full text-left text-sm">
			<thead>
				<tr class="border-b border-white/20">
					<th class="pb-3 pr-4 font-semibold text-white">Name</th>
					<th class="pb-3 pr-4 font-semibold text-white">Skills</th>
					<th class="pb-3 font-semibold text-white">E-Mail</th>
				</tr>
			</thead>
			<tbody>
				{#each applications as app}
					<tr class="border-b border-white/10">
						<td class="py-3 pr-4 text-white/90">{app.name}</td>
						<td class="py-3 pr-4 text-white/70">{app.skills.join(', ')}</td>
						<td class="py-3 text-white/70">{app.email}</td>
					</tr>
				{/each}
			</tbody>
		</table>

		{#if applications.length === 0}
			<p class="text-center text-white/50 py-8">Keine Bewerbungen gefunden</p>
		{/if}
	</div>
</div>