import { useMemo, useState } from 'react'
import './App.css'

const samples = [
  {
    id: 1,
    title: 'Moonlit Library',
    character: 'Lina',
    tags: ['portrait', 'library', 'warm light'],
    accent: 'amber',
    prompt:
      'masterpiece, best quality, 1girl, silver hair, moonlit library, warm candle light, detailed eyes',
    negativePrompt: 'low quality, blurry, bad anatomy, extra fingers',
  },
  {
    id: 2,
    title: 'Rainy Neon Street',
    character: 'Mika',
    tags: ['cyberpunk', 'rain', 'city'],
    accent: 'teal',
    prompt:
      'masterpiece, best quality, 1girl, short black hair, neon street, rain, reflective pavement',
    negativePrompt: 'worst quality, jpeg artifacts, bad hands, watermark',
  },
  {
    id: 3,
    title: 'Garden Tea Time',
    character: 'Noel',
    tags: ['garden', 'dress', 'soft color'],
    accent: 'rose',
    prompt:
      'masterpiece, best quality, 1girl, frilled dress, flower garden, afternoon tea, soft sunlight',
    negativePrompt: 'lowres, text, logo, missing fingers, deformed',
  },
]

function App() {
  const [query, setQuery] = useState('')
  const [copiedId, setCopiedId] = useState(null)

  const filteredSamples = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase()
    if (!normalizedQuery) return samples

    return samples.filter((sample) => {
      const searchableText = [
        sample.title,
        sample.character,
        sample.prompt,
        sample.negativePrompt,
        ...sample.tags,
      ]
        .join(' ')
        .toLowerCase()

      return searchableText.includes(normalizedQuery)
    })
  }, [query])

  const copyPrompt = async (sample) => {
    const text = `${sample.prompt}\nNegative prompt: ${sample.negativePrompt}`

    try {
      await navigator.clipboard.writeText(text)
      setCopiedId(sample.id)
      window.setTimeout(() => setCopiedId(null), 1600)
    } catch {
      setCopiedId(null)
    }
  }

  return (
    <main className="app-shell">
      <header className="top-bar">
        <div>
          <p className="eyebrow">NovelAI prompt manager</p>
          <h1>Prompt Gallery</h1>
        </div>
        <div className="summary-pill">{filteredSamples.length} images</div>
      </header>

      <section className="toolbar" aria-label="Gallery filters">
        <label className="search-field">
          <span>Search</span>
          <input
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="prompt, tag, character"
          />
        </label>
      </section>

      <section className="gallery-grid" aria-label="Prompt gallery">
        {filteredSamples.map((sample) => (
          <article className="prompt-card" key={sample.id}>
            <div className={`art-preview ${sample.accent}`}>
              <div className="art-glow" />
              <div className="art-frame">
                <span>{sample.character}</span>
              </div>
            </div>

            <div className="card-body">
              <div className="card-heading">
                <div>
                  <h2>{sample.title}</h2>
                  <p>{sample.character}</p>
                </div>
                <button type="button" onClick={() => copyPrompt(sample)}>
                  {copiedId === sample.id ? 'Copied' : 'Copy'}
                </button>
              </div>

              <div className="tag-row">
                {sample.tags.map((tag) => (
                  <span key={tag}>{tag}</span>
                ))}
              </div>

              <p className="prompt-text">{sample.prompt}</p>
            </div>
          </article>
        ))}
      </section>
    </main>
  )
}

export default App
