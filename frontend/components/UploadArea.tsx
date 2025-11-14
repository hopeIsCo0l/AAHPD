'use client';

import { useState, useRef } from 'react';
import Image from 'next/image';

interface UploadAreaProps {
  onFileSelect: (file: File) => void;
  isAnalyzing?: boolean;
}

export default function UploadArea({ onFileSelect, isAnalyzing = false }: UploadAreaProps) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleClick = () => {
    if (!isAnalyzing) {
      fileInputRef.current?.click();
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onFileSelect(file);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) {
      onFileSelect(file);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  if (isAnalyzing) {
    return (
      <div className="flex flex-col gap-2">
        <h2 className="text-base font-medium text-[#0d0f11] leading-6">Analyzing your document</h2>
        <div className="bg-[#f7f8f9] border border-[#d0d5dd] rounded-lg h-[170px] flex items-center justify-center relative overflow-hidden cursor-default">
          <Image
            src="http://localhost:3845/assets/c61d21c7598593db9038249c62c561759f631afd.svg"
            alt=""
            width={1171}
            height={839}
            className="absolute left-[-192px] top-[-330px] opacity-10 pointer-events-none"
          />
          <div className="flex flex-col items-center gap-2 text-center z-10">
            <Image
              src="http://localhost:3845/assets/dac3e080659cd842fed7ff22130786209b0bbf71.svg"
              alt=""
              width={24}
              height={24}
            />
            <div className="text-sm font-semibold text-[#1d4ed8] leading-[21px]">Analyzing your document...</div>
            <div className="text-xs text-[#112f82] leading-[21px]">This may take a few moment</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-2">
      <h2 className="text-base font-medium text-[#0d0f11] leading-6">Start a New Analysis</h2>
      <div
        onClick={handleClick}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`bg-[#f7f8f9] border border-dashed rounded-lg h-[170px] flex items-center justify-center px-6 py-11 cursor-pointer transition-all ${
          isDragging
            ? 'border-[#1d4ed8] bg-[#e8edfb]'
            : 'border-[#d0d5dd] hover:border-[#1d4ed8] hover:bg-[#e8edfb]'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx"
          onChange={handleFileChange}
          className="hidden"
        />
        <div className="flex flex-col items-center gap-2 text-center">
          <Image
            src="http://localhost:3845/assets/51a134b88543a30b1954ff16a624ddb9cb10056c.svg"
            alt=""
            width={24}
            height={24}
          />
          <div className="text-sm leading-[21px] text-[#0d0f11]">
            <span className="font-semibold">Click to upload your assignment</span>
            <span> or drag and drop</span>
          </div>
          <div className="text-xs text-[#64748b] leading-[21px]">PDF, DOCX up to 10MB</div>
        </div>
      </div>
    </div>
  );
}

