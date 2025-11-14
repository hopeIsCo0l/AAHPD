'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';

export default function SignupPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    fullName: '',
    studentId: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const submitData = new FormData();
      submitData.append('email', formData.email);
      submitData.append('password', formData.password);
      submitData.append('full_name', formData.fullName);
      submitData.append('student_id', formData.studentId || '');

      const response = await fetch('/api/auth/register', {
        method: 'POST',
        body: submitData,
      });

      if (response.ok) {
        router.push('/login');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Registration failed');
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

      {/* Signup Card */}
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
            <h1 className="text-[25px] font-medium text-black leading-[30px]">Create Account</h1>
            <p className="text-sm text-[#64748b] leading-[21px] mt-0">
              Simplify your studies with AI-powered writing help and plagiarism detection.
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
                name="email"
                value={formData.email}
                onChange={handleChange}
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
                name="password"
                value={formData.password}
                onChange={handleChange}
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

            {/* Full Name */}
            <div className="bg-[#f3f7fa] rounded-xl px-4 py-3 flex items-center gap-1 focus-within:bg-white focus-within:shadow-[0_0_0_1px_#587bf6] transition-all">
              <Image
                src="http://localhost:3845/assets/e874fedc969dc37b615c9798d8c814e68c4911ce.svg"
                alt=""
                width={24}
                height={24}
              />
              <input
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                placeholder="Full Name"
                required
                className="flex-1 bg-transparent border-none outline-none text-sm font-medium text-[#64748b] placeholder:text-[#64748b]"
              />
            </div>

            {/* Student ID */}
            <div className="bg-[#f3f7fa] rounded-xl px-4 py-3 flex items-center gap-1 focus-within:bg-white focus-within:shadow-[0_0_0_1px_#587bf6] transition-all">
              <Image
                src="http://localhost:3845/assets/e874fedc969dc37b615c9798d8c814e68c4911ce.svg"
                alt=""
                width={24}
                height={24}
              />
              <input
                type="text"
                name="studentId"
                value={formData.studentId}
                onChange={handleChange}
                placeholder="Student ID (Optional)"
                className="flex-1 bg-transparent border-none outline-none text-sm font-medium text-[#64748b] placeholder:text-[#64748b]"
              />
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
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        {/* Login Link */}
        <p className="text-sm text-[#64748b] text-center">
          Already have an account?{' '}
          <Link href="/login" className="text-[#587bf6] font-semibold underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}

