<script lang="ts">
  import type { Application, AIProvider } from '$lib/types';

  type ProviderBlock = {
    provider: AIProvider;
    applications: Application[];
    metadata?: { answerTime?: number; tokens?: number };
  };

  export let providers: ProviderBlock[] = [];
  export let columns: string[] = ['Name', 'Skills', 'E‑Mail', 'Position'];

  const formatTime = (ms?: number) => (typeof ms === 'number' ? `${ms}ms` : '—');
  const formatTokens = (t?: number) => (typeof t === 'number' ? String(t) : '—');

  const initials = (name: string) =>
    name
      .split(' ')
      .map((p) => p[0]?.toUpperCase() ?? '')
      .slice(0, 2)
      .join('');
</script>

{#if providers.length === 0}
  <div class="w-full max-w-4xl mx-auto">
    <div class="rounded-lg border border-white/20 bg-white/03 p-6 text-center text-sm text-white/70">Keine Ergebnisse</div>
  </div>
{:else}
  <div class="grid gap-6 md:grid-cols-2">
    {#each providers as block (block.provider.name)}
      <section class="relative rounded-2xl p-6 bg-white/05 backdrop-blur-md border border-white/20">
        <div class="flex items-start gap-4 mb-7">
          {#if block.provider.icon}
            <img src={block.provider.icon} alt={block.provider.name} class="w-10 h-10 object-contain" />
          {:else}
            <div class="w-10 h-10 rounded-md bg-white/06 flex items-center justify-center text-sm font-semibold text-white/90">{initials(block.provider.name)}</div>
          {/if}

			<div class="flex-1 min-w-0">
				<div class="flex items-center justify-between">
				<h3 class="text-lg font-semibold text-white truncate">{block.provider.name}</h3>
				</div>
			</div>

			<div class="flex-1">
				<p class="flex mt-1 text-xs text-white/70">
					Antwortzeit: 
					<span class="font-medium text-white">{formatTime(block.metadata?.answerTime)}</span> 
				</p>
				<p class="flex mt-1 text-xs text-white/70">
					Tokens: 
					<span class="font-medium text-white">{formatTokens(block.metadata?.tokens)}</span>
				</p>
			</div>
        </div>

		

        <div class="mt-4">

            <div class="grid">
              <div class="flex w-full">
                  {#each columns as col}
                    <div class="px-2 pb-3 text-xs font-medium uppercase" style="flex:1">
                      {#if columns.includes(col)}
                        <span class="text-white/80">{col}</span>
                      {:else}
                        <span class="text-white/40">{col}</span>
                      {/if}
                    </div>
                  {/each}
              </div>
            </div>

            {#if block.applications && block.applications.length > 0}
              <div class="divide-y divide-white/06 mt-2 rounded-md overflow-hidden">
                {#each block.applications as app}
                  <div class="grid hover:bg-white/01" style={"grid-template-columns: repeat(" + columns.length + ", minmax(0, 1fr))"}>
                    {#each columns as col}
                      {#if !columns.includes(col)}
                        <div class="text-sm text-white/30 px-3 py-3">—</div>
                      {:else if col === 'Name'}
                        <div class="text-sm text-white truncate px-3 py-3">{app.name}</div>
                      {:else if col === 'Skills'}
                        <div class="text-sm text-white/90 px-3 py-3">{app.skills.join(', ')}</div>
                      {:else if col === 'E-Mail' || col === 'E‑Mail' || col === 'Email'}
                        <div class="text-sm text-white/80 px-3 py-3">{app.email}</div>
                      {:else if col === 'Position'}
                        <div class="text-sm text-white/80 px-3 py-3">{app.position ?? '—'}</div>
                      {:else}
                        <div class="text-sm text-white/80 px-3 py-3">{(app as any)[col.toLowerCase()] ?? '—'}</div>
                      {/if}
                    {/each}
                  </div>
                {/each}
              </div>
            {:else}
              <div class="px-3 py-4 text-sm text-white/70">Keine Bewerbungen vorhanden.</div>
            {/if}

        </div>
      </section>
    {/each}
  </div>
{/if}
