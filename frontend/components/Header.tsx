'use client';

import Image from 'next/image';

interface HeaderProps {
  title: string;
  subtitle?: string;
  actionButton?: {
    label: string;
    icon: string;
    onClick: () => void;
  };
}

export default function Header({ title, subtitle, actionButton }: HeaderProps) {
  return (
    <div className="bg-white border-b border-[#e7eaee] px-8 py-8 flex items-center justify-between">
      <div className="flex flex-col gap-1">
        <h1 className="text-[25px] font-semibold text-black leading-[30px]">{title}</h1>
        {subtitle && (
          <p className="text-base text-[#64748b] leading-6">{subtitle}</p>
        )}
      </div>
      {actionButton && (
        <button
          onClick={actionButton.onClick}
          className="bg-[#587bf6] border border-[#ced7ea] rounded-lg px-6 py-2 flex items-center gap-3 text-white text-sm font-semibold hover:bg-[#4a6ef5] transition-colors"
        >
          <Image src={actionButton.icon} alt="" width={24} height={24} />
          <span>{actionButton.label}</span>
        </button>
      )}
    </div>
  );
}

