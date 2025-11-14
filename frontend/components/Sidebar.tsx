'use client';

import Image from 'next/image';
import { usePathname, useRouter } from 'next/navigation';

interface NavItem {
  icon: string;
  label: string;
  path: string;
}

const mainMenuItems: NavItem[] = [
  {
    icon: 'http://localhost:3845/assets/28388eacd5deafb10859bc1f9faf74a5b64d5e07.svg',
    label: 'Assignment Analysis',
    path: '/dashboard/analysis',
  },
  {
    icon: 'http://localhost:3845/assets/af032e3753638ba2e5babae573d024fdbf3d4877.svg',
    label: 'Source Search',
    path: '/dashboard/sources',
  },
  {
    icon: 'http://localhost:3845/assets/b52496381cb52cd2d13843eee06e3558b3097cc4.svg',
    label: 'Previous Queries',
    path: '/dashboard/history',
  },
];

export default function Sidebar({ userName = 'Abdella Teshome', userEmail = 'Abdella@gmail.com' }: { userName?: string; userEmail?: string }) {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userName');
    router.push('/login');
  };

  return (
    <div className="fixed left-0 top-0 h-screen w-64 bg-white border-r border-[#e7eaee] flex flex-col gap-[42px] px-4 py-8">
      {/* Logo */}
      <div className="flex items-center gap-4">
        <Image
          src="http://localhost:3845/assets/1fc63e63b0005cab58a6026b3398f3903dca409e.svg"
          alt="Company Logo"
          width={44}
          height={44}
          className="w-11 h-11"
        />
      </div>

      {/* Main Menu */}
      <div className="flex flex-col gap-4">
        <div className="px-3 text-sm text-[#64748b]">Main Menu</div>
        <div className="flex flex-col gap-2">
          {mainMenuItems.map((item) => {
            const isActive = pathname === item.path;
            return (
              <button
                key={item.path}
                onClick={() => router.push(item.path)}
                className={`flex items-center gap-3 px-3 py-3 rounded-xl transition-all ${
                  isActive
                    ? 'bg-[#e8edfb] text-[#1d4ed8] font-medium'
                    : 'bg-white text-[#4b5768] hover:bg-[#f7f8f9]'
                }`}
              >
                <Image src={item.icon} alt="" width={24} height={24} />
                <span className="text-base">{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* General Section */}
      <div className="flex-1 flex flex-col justify-end gap-4 border-t border-[#e7eaee] pt-6">
        <div className="flex flex-col gap-4">
          <div className="px-3 text-sm text-[#64748b]">General</div>
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 px-3 py-3 rounded-xl bg-white text-[#f54900] hover:bg-[#f7f8f9] transition-all"
          >
            <Image
              src="http://localhost:3845/assets/a81e48721c8436fab457ff13a580bae82517a886.svg"
              alt=""
              width={24}
              height={24}
            />
            <span className="text-base">Logout</span>
          </button>
        </div>

        {/* User Profile */}
        <div className="flex items-end gap-4 mt-auto">
          <div className="w-11 h-11 rounded-full border-[0.5px] border-[rgba(158,212,250,0.5)] bg-[#88aeff] flex items-center justify-center overflow-hidden flex-shrink-0">
            <Image
              src="http://localhost:3845/assets/9ee507647e4d2aaf280cc033e07e6f9cf688846f.png"
              alt="User"
              width={39}
              height={39}
              className="object-cover"
            />
          </div>
          <div className="flex-1 flex flex-col">
            <div className="text-lg font-medium text-black leading-[27px]">{userName}</div>
            <div className="text-sm text-[#64748b] leading-[21px]">{userEmail}</div>
          </div>
        </div>
      </div>
    </div>
  );
}

