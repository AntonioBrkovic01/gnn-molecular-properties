import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

function App() {
  const [smiles, setSmiles] = useState('')
  const [examples, setExamples] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)
  const [moleculeImage, setMoleculeImage] = useState(null)

  useEffect(() => {
    axios.get(`${API_URL}/examples`)
      .then(res => setExamples(res.data.examples))
      .catch(err => console.error('Greška pri učitavanju primjera:', err))
  }, [])

  const handlePredict = async () => {
    if (!smiles.trim()) {
      setError('Unesi SMILES notaciju molekule')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)
    setMoleculeImage(null)

    try {
      const [predictRes, imageRes] = await Promise.all([
        axios.post(`${API_URL}/predict`, { smiles }),
        axios.post(`${API_URL}/molecule-image`, { smiles }),
      ])

      setResult(predictRes.data)
      setMoleculeImage(imageRes.data.image)
    } catch (err) {
      setError(err.response?.data?.detail || 'Greška pri predikciji')
    } finally {
      setLoading(false)
    }
  }

  const handleExampleClick = (exampleSmiles) => {
    setSmiles(exampleSmiles)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-8 px-4">
      <div className="max-w-5xl mx-auto">
        <header className="text-center mb-10">
          <h1 className="text-4xl font-bold text-slate-800 mb-2">
            Predikcija svojstava molekula
          </h1>
          <p className="text-slate-600">
            Grafovska neuronska mreža za predviđanje topljivosti i toksičnosti
          </p>
        </header>

        <div className="bg-white rounded-xl shadow-md p-6 mb-6">
          <label className="block text-sm font-medium text-slate-700 mb-2">
            SMILES notacija molekule
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={smiles}
              onChange={(e) => setSmiles(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handlePredict()}
              placeholder="npr. CCO (etanol)"
              className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none font-mono"
            />
            <button
              onClick={handlePredict}
              disabled={loading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-slate-400 transition font-medium"
            >
              {loading ? 'Računam...' : 'Predvidi'}
            </button>
          </div>

          {examples.length > 0 && (
            <div className="mt-4">
              <p className="text-xs text-slate-500 mb-2">Primjeri:</p>
              <div className="flex flex-wrap gap-2">
                {examples.map((ex) => (
                  <button
                    key={ex.smiles}
                    onClick={() => handleExampleClick(ex.smiles)}
                    className="text-xs px-3 py-1 bg-slate-100 hover:bg-slate-200 rounded-full text-slate-700 transition"
                    title={ex.description}
                  >
                    {ex.name}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {result && (
          <div className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-lg font-semibold text-slate-800 mb-3">
                  Struktura molekule
                </h2>
                {moleculeImage && (
                  <img
                    src={moleculeImage}
                    alt="Molekula"
                    className="w-full max-w-xs mx-auto"
                  />
                )}
                <p className="text-xs text-slate-500 font-mono text-center mt-2 break-all">
                  {result.smiles}
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-lg font-semibold text-slate-800 mb-3">
                  Topljivost
                </h2>
                <div className="text-4xl font-bold text-blue-600 mb-1">
                  {result.solubility.toFixed(2)}
                </div>
                <div className="text-sm text-slate-500 mb-3">log mol/L</div>
                <div className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                  {result.solubility_category}
                </div>
                <div className="mt-4 pt-4 border-t border-slate-100">
                  <p className="text-xs text-slate-500">
                    Veće vrijednosti = bolje topljivo u vodi
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-lg font-semibold text-slate-800 mb-3">
                Toksičnost
              </h2>
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <div className="text-sm text-slate-500">Prosječni rizik</div>
                  <div className="text-2xl font-bold text-slate-800">
                    {(result.avg_toxicity_risk * 100).toFixed(1)}%
                  </div>
                </div>
                <div>
                  <div className="text-sm text-slate-500">Visokorizičnih taskova</div>
                  <div className="text-2xl font-bold text-slate-800">
                    {result.high_risk_count} / 12
                  </div>
                </div>
              </div>

              <div className="space-y-2">
                {result.toxicity_tasks.map((task) => (
                  <div key={task.task} className="flex items-center gap-3">
                    <div className="w-32 text-sm font-medium text-slate-700">
                      {task.task}
                    </div>
                    <div className="flex-1 bg-slate-100 rounded-full h-6 overflow-hidden">
                      <div
                        className={`h-full transition-all duration-500 ${
                          task.probability > 0.5
                            ? 'bg-red-500'
                            : task.probability > 0.25
                            ? 'bg-yellow-500'
                            : 'bg-green-500'
                        }`}
                        style={{ width: `${task.probability * 100}%` }}
                      />
                    </div>
                    <div className="w-16 text-right text-sm font-mono text-slate-600">
                      {(task.probability * 100).toFixed(1)}%
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-4 pt-4 border-t border-slate-100 flex gap-4 text-xs text-slate-500">
                <div className="flex items-center gap-1">
                  <span className="w-3 h-3 bg-green-500 rounded-full"></span>
                  Nizak rizik (ispod 25%)
                </div>
                <div className="flex items-center gap-1">
                  <span className="w-3 h-3 bg-yellow-500 rounded-full"></span>
                  Srednji rizik (25-50%)
                </div>
                <div className="flex items-center gap-1">
                  <span className="w-3 h-3 bg-red-500 rounded-full"></span>
                  Visok rizik (iznad 50%)
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App