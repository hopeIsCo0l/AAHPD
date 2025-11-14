'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('email', email);
      formData.append('password', password);

      const response = await fetch('/api/auth/login', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('authToken', data.access_token);
        localStorage.setItem('userEmail', email);
        localStorage.setItem('userName', email.split('@')[0]);
        router.push('/dashboard/analysis');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Login failed');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f3f4fa] flex items-center justify-center relative overflow-hidden">
      {/* Background Images */}
      <Image
        src="http://localhost:3845/assets/1a1faf3c7f8271a35ff3660559873abcc2e667e7.svg"
        alt=""
        fill
        className="absolute top-[-194px] left-[-451px] w-[2107px] h-[1539px] z-0 pointer-events-none"
        style={{ objectFit: 'none' }}
      />
      <Image
        src="http://localhost:3845/assets/4e2d7d06493135825e41ee752d5aa83528fa604c.svg"
        alt=""
        fill
        className="absolute top-[-81px] left-[44px] w-[1352px] h-[1185px] z-0 opacity-10 pointer-events-none"
        style={{ objectFit: 'none' }}
      />

      {/* Login Card */}
      <div className="bg-white border border-[#e2eafb] rounded-3xl p-11 w-full max-w-[444px] relative z-10 flex flex-col gap-8">
        {/* Logo and Header */}
        <div className="flex flex-col gap-4 items-center">
          <Image
            src="http://localhost:3845/assets/19d440781b6b42884d6f4a65be3b198d408189e4.svg"
            alt="Logo"
            width={51}
            height={51}
          />
          <div className="flex flex-col items-center text-center">
            <h1 className="text-[25px] font-medium text-black leading-[30px]">Welcome back</h1>
            <p className="text-sm text-[#64748b] leading-[21px] mt-0">
              Continue improving your assignments with<br />smart AI assistance.
            </p>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-5">
          <div className="flex flex-col gap-3">
            {/* Email */}
            <div className="bg-[#f3f7fa] rounded-xl px-4 py-3 flex items-center gap-1 focus-within:bg-white focus-within:shadow-[0_0_0_1px_#587bf6] transition-all">
              <Image
                src="http://localhost:3845/assets/e874fedc969dc37b615c9798d8c814e68c4911ce.svg"
                alt=""
                width={24}
                height={24}
              />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
                required
                className="flex-1 bg-transparent border-none outline-none text-sm font-medium text-[#64748b] placeholder:text-[#64748b]"
              />
            </div>

            {/* Password */}
            <div className="bg-[#f3f7fa] rounded-xl px-4 py-3 flex items-center gap-1 focus-within:bg-white focus-within:shadow-[0_0_0_1px_#587bf6] transition-all">
              <Image
                src="http://localhost:3845/assets/e197d5426c46729d04eaa255a13aec6c5ba6644d.svg"
                alt=""
                width={24}
                height={24}
              />
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                required
                className="flex-1 bg-transparent border-none outline-none text-sm font-medium text-[#64748b] placeholder:text-[#64748b]"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="w-6 h-6 flex items-center justify-center"
              >
                <Image
                  src="http://localhost:3845/assets/980a63f668b16d6a007238c2c4fe1715aca3df28.svg"
                  alt=""
                  width={24}
                  height={24}
                />
              </button>
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="bg-[#587bf6] border border-[#ced7ea] rounded-xl py-3 px-8 text-white text-base font-semibold hover:bg-[#4a6ef5] transition-colors disabled:opacity-50"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        {/* Signup Link */}
        <p className="text-sm text-[#64748b] text-center">
          Don't have an account?{' '}
          <Link href="/signup" className="text-[#587bf6] font-semibold underline">
            Signup
          </Link>
        </p>
      </div>
    </div>
  );
}

