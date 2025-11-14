'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import UploadArea from '@/components/UploadArea';
import Image from 'next/image';

export default function AnalysisPage() {
  const router = useRouter();
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResults, setAnalysisResults] = useState<any>(null);
  const [academicLevel, setAcademicLevel] = useState('');
  const [topic, setTopic] = useState('');

  const handleFileSelect = async (file: File) => {
    setIsAnalyzing(true);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (academicLevel) formData.append('academic_level', academicLevel);
      if (topic) formData.append('topic', topic);

      const token = localStorage.getItem('authToken');
      const response = await fetch('/api/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        // Poll for results
        setTimeout(() => {
          checkAnalysis(data.assignment_id);
        }, 2000);
      } else {
        setIsAnalyzing(false);
        alert('Upload failed');
      }
    } catch (error) {
      setIsAnalyzing(false);
      alert('Error uploading file');
    }
  };

  const checkAnalysis = async (assignmentId: string) => {
    const token = localStorage.getItem('authToken');
    const response = await fetch(`/api/analysis/${assignmentId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (response.ok) {
      const data = await response.json();
      setAnalysisResults(data);
      setIsAnalyzing(false);
    } else {
      setTimeout(() => checkAnalysis(assignmentId), 3000);
    }
  };

  return (
    <>
      <Header
        title="Assignment Analysis"
        subtitle="Review your work and detect plagiarism with AI precision."
        actionButton={{
          label: 'Upload Assignment',
          icon: 'http://localhost:3845/assets/9f9c1494c8c9c21c6d86216a676b73466abe956d.svg',
          onClick: () => document.getElementById('file-input')?.click(),
        }}
      />
      
      <div className="p-8 flex flex-col gap-8">
        {!analysisResults && (
          <div className="bg-white border border-[#e7eaee] rounded-lg p-8 flex flex-col gap-8">
            <UploadArea onFileSelect={handleFileSelect} isAnalyzing={isAnalyzing} />
            
            <div className="flex gap-8 items-start">
              <div className="flex flex-col gap-2 w-[202px]">
                <label className="text-base font-medium text-[#0d0f11] leading-6">
                  Academic Level (Optional)
                </label>
                <select
                  value={academicLevel}
                  onChange={(e) => setAcademicLevel(e.target.value)}
                  className="bg-white border border-[#e7eaee] rounded-lg px-3 py-2 text-sm text-[#0d0f11] cursor-pointer"
                >
                  <option value="">Select Level</option>
                  <option value="High School">High School</option>
                  <option value="Undergraduate">Undergraduate</option>
                  <option value="Graduate">Graduate</option>
                  <option value="PhD">PhD</option>
                </select>
              </div>
              
              <div className="flex-1 flex flex-col gap-2">
                <label className="text-base font-medium text-[#0d0f11] leading-6">
                  Topic/Title (Optional)
                </label>
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="e.g Climate Change Research"
                  className="bg-white border border-[#e7eaee] rounded-lg px-4 py-2 text-sm text-[#0d0f11]"
                />
              </div>
            </div>
          </div>
        )}

        {analysisResults && (
          <>
            {/* Report */}
            <div className="bg-white border border-[#e7eaee] rounded-lg p-8 flex flex-col gap-8">
              <div className="flex flex-col gap-2">
                <h2 className="text-base font-medium text-[#0d0f11] leading-6">
                  <span className="text-[#64748b]">Analysis Report:</span>{' '}
                  {analysisResults.filename || 'Assignment'}
                </h2>
                
                {/* Score Cards */}
                <div className="flex gap-3">
                  <div className="flex-1 border border-[#e7eaee] rounded-lg p-8 flex flex-col gap-6 relative overflow-hidden bg-[#dae2ff]">
                    <Image
                      src="http://localhost:3845/assets/66288337665019b6a9dd2ee361a3b486c34cb443.png"
                      alt=""
                      fill
                      className="absolute opacity-30 pointer-events-none"
                      style={{ objectFit: 'cover' }}
                    />
                    <div className="flex justify-between items-start relative z-10">
                      <div className="text-lg font-medium text-[#0d0f11] leading-[27px]">Plagiarism Score</div>
                      <div className="bg-[#e8edfb] border-[0.5px] border-[#bbcaf3] rounded-lg p-2">
                        <Image
                          src="http://localhost:3845/assets/b6059ba467dbd1cc3e320568633057ee685ad55c.svg"
                          alt=""
                          width={16}
                          height={16}
                        />
                      </div>
                    </div>
                    <div className="text-[39px] font-medium text-[#1d4ed8] leading-[42.9px] relative z-10">
                      {Math.round((analysisResults.analysis?.plagiarism_score || 0) * 100)}%
                    </div>
                  </div>
                  
                  <div className="flex-1 border border-[#e7eaee] rounded-lg p-8 flex flex-col gap-6 relative overflow-hidden bg-[#dae2ff]">
                    <Image
                      src="http://localhost:3845/assets/66288337665019b6a9dd2ee361a3b486c34cb443.png"
                      alt=""
                      fill
                      className="absolute opacity-30 pointer-events-none"
                      style={{ objectFit: 'cover' }}
                    />
                    <div className="flex justify-between items-start relative z-10">
                      <div className="text-lg font-medium text-[#0d0f11] leading-[27px]">Confidence Score</div>
                      <div className="bg-[#e8edfb] border-[0.5px] border-[#bbcaf3] rounded-lg p-2">
                        <Image
                          src="http://localhost:3845/assets/1cb672dc72bbf18091b9673449930839421617f8.svg"
                          alt=""
                          width={16}
                          height={16}
                        />
                      </div>
                    </div>
                    <div className="text-[39px] font-medium text-[#1d4ed8] leading-[42.9px] relative z-10">
                      {Math.round((analysisResults.analysis?.confidence_score || 0) * 100)}%
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Info Cards */}
              <div className="flex gap-3">
                <div className="flex-1 bg-[#f7f8f9] border border-[#e7eaee] rounded-lg py-2 flex flex-col gap-1 text-center">
                  <div className="text-sm text-[#64748b] leading-6">Topic</div>
                  <div className="text-base font-medium text-[#0d0f11] leading-6">
                    {analysisResults.topic || 'Unknown'}
                  </div>
                </div>
                <div className="flex-1 bg-[#f7f8f9] border border-[#e7eaee] rounded-lg py-2 flex flex-col gap-1 text-center">
                  <div className="text-sm text-[#64748b] leading-6">Academic Level</div>
                  <div className="text-base font-medium text-[#0d0f11] leading-6">
                    {analysisResults.academic_level || 'Unknown'}
                  </div>
                </div>
                <div className="flex-1 bg-[#f7f8f9] border border-[#e7eaee] rounded-lg py-2 flex flex-col gap-1 text-center">
                  <div className="text-sm text-[#64748b] leading-6">Word Count</div>
                  <div className="text-base font-medium text-[#0d0f11] leading-6">
                    {analysisResults.word_count || '0'}
                  </div>
                </div>
              </div>
            </div>

            {/* Suggestions */}
            <div className="flex gap-3">
              <div className="flex-1 bg-white border border-[#e7eaee] rounded-lg p-8 relative overflow-hidden">
                <Image
                  src="http://localhost:3845/assets/278e01a358d64538256a0c77f33e62fc4e4a5659.svg"
                  alt=""
                  fill
                  className="absolute left-[-452px] top-[-234px] opacity-10 pointer-events-none"
                  style={{ objectFit: 'none' }}
                />
                <div className="flex justify-between items-start mb-2 relative z-10">
                  <div className="text-base font-medium text-[#0d0f11] leading-6">AI Based Suggestions</div>
                  <Image
                    src="http://localhost:3845/assets/a973e85d73515885dfc940c0eaf7c8de3bd920d4.svg"
                    alt=""
                    width={24}
                    height={24}
                  />
                </div>
                <div className="bg-white border border-[#f7f8f9] rounded-lg p-6 relative z-10">
                  <div className="flex flex-col gap-5">
                    <div className="flex flex-col gap-1">
                      <div className="text-base font-semibold text-[#0d0f11] leading-6">Next Steps</div>
                      <div className="text-sm text-[#64748b] leading-5">
                        {analysisResults.analysis?.research_suggestions || 'No suggestions available.'}
                      </div>
                    </div>
                    <button
                      onClick={() => router.push('/dashboard/sources')}
                      className="bg-[#1d4ed8] border border-[#e7eaee] rounded-lg px-6 py-1 text-white text-sm font-medium hover:bg-[#1e40af] transition-colors self-end"
                    >
                      Explore sources
                    </button>
                  </div>
                </div>
              </div>
              
              <div className="flex-1 bg-[#f7f8f9] border border-[#e7eaee] rounded-lg p-8">
                <div className="text-base font-medium text-[#0d0f11] leading-6 mb-2">Citation Compliance</div>
                <div className="bg-white border border-[#e7eaee] rounded-lg p-6">
                  <div className="flex flex-col gap-5">
                    <div className="flex flex-col gap-2">
                      <div className="text-base font-semibold text-[#0d0f11] leading-6">Citation Standards</div>
                      <div className="text-sm text-[#64748b] leading-5">
                        {analysisResults.analysis?.citation_recommendations || 'Use APA format for citations, Ensure all sources are properly cited and referenced'}
                      </div>
                    </div>
                    <button className="bg-[#1d4ed8] border border-[#e7eaee] rounded-lg px-6 py-1 text-white text-sm font-medium hover:bg-[#1e40af] transition-colors self-end">
                      View citation guide
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </>
  );
}

