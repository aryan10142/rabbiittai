"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Status = "idle" | "loading" | "success" | "error";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [message, setMessage] = useState("");
  const [preview, setPreview] = useState("");

  const onDrop = useCallback((accepted: File[]) => {
    if (accepted.length > 0) {
      setFile(accepted[0]);
      setStatus("idle");
      setMessage("");
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "text/csv": [".csv"],
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
        ".xlsx",
      ],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !email) return;

    setStatus("loading");
    setMessage("");
    setPreview("");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("email", email);

    try {
      const res = await fetch(`${API_URL}/api/analyze`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        setStatus("error");
        setMessage(data.detail || "Something went wrong.");
        return;
      }

      setStatus("success");
      setMessage(data.message);
      setPreview(data.summary_preview || "");
    } catch {
      setStatus("error");
      setMessage("Network error. Please try again.");
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center px-4 py-12">
      <div className="w-full max-w-lg space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-4xl font-bold tracking-tight text-white">
            Sales Insight <span className="text-indigo-400">Automator</span>
          </h1>
          <p className="mt-2 text-gray-400">
            Upload your sales data &amp; get an AI-generated brief sent to your
            inbox.
          </p>
        </div>

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="rounded-2xl border border-gray-800 bg-gray-900 p-6 shadow-xl space-y-6"
        >
          {/* Dropzone */}
          <div
            {...getRootProps()}
            className={`flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-8 transition-colors ${
              isDragActive
                ? "border-indigo-400 bg-indigo-950/30"
                : file
                ? "border-green-500 bg-green-950/20"
                : "border-gray-700 hover:border-gray-500"
            }`}
          >
            <input {...getInputProps()} />
            {file ? (
              <div className="text-center">
                <svg
                  className="mx-auto h-8 w-8 text-green-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <p className="mt-2 text-sm font-medium text-green-300">
                  {file.name}
                </p>
                <p className="text-xs text-gray-500">
                  {(file.size / 1024).toFixed(1)} KB — click or drag to replace
                </p>
              </div>
            ) : (
              <div className="text-center">
                <svg
                  className="mx-auto h-10 w-10 text-gray-500"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  />
                </svg>
                <p className="mt-2 text-sm text-gray-400">
                  Drag &amp; drop a <strong>.csv</strong> or{" "}
                  <strong>.xlsx</strong> file here
                </p>
                <p className="text-xs text-gray-600">or click to browse</p>
              </div>
            )}
          </div>

          {/* Email */}
          <div>
            <label
              htmlFor="email"
              className="mb-1 block text-sm font-medium text-gray-300"
            >
              Recipient Email
            </label>
            <input
              id="email"
              type="email"
              required
              placeholder="you@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-lg border border-gray-700 bg-gray-800 px-4 py-2.5 text-sm text-white placeholder-gray-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={!file || !email || status === "loading"}
            className="w-full rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {status === "loading" ? (
              <span className="flex items-center justify-center gap-2">
                <svg
                  className="h-4 w-4 animate-spin"
                  viewBox="0 0 24 24"
                  fill="none"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                  />
                </svg>
                Analyzing &amp; Sending…
              </span>
            ) : (
              "Generate & Send Summary"
            )}
          </button>

          {/* Status Messages */}
          {status === "success" && (
            <div className="rounded-lg border border-green-800 bg-green-950/40 p-4 text-sm text-green-300">
              ✓ {message}
            </div>
          )}
          {status === "error" && (
            <div className="rounded-lg border border-red-800 bg-red-950/40 p-4 text-sm text-red-300">
              ✗ {message}
            </div>
          )}
        </form>

        {/* Summary preview */}
        {preview && (
          <div className="rounded-2xl border border-gray-800 bg-gray-900 p-6 shadow-xl">
            <h2 className="mb-3 text-lg font-semibold text-gray-200">
              Summary Preview
            </h2>
            <div
              className="prose prose-invert prose-sm max-w-none"
              dangerouslySetInnerHTML={{ __html: preview }}
            />
          </div>
        )}

        {/* Footer */}
        <p className="text-center text-xs text-gray-600">
          Powered by Rabbitt AI · Groq · Resend
        </p>
      </div>
    </main>
  );
}
