import Link from 'next/link';
import Header from '@/components/header.js';

function PropExample(props) {
    return <p className='text-center'>Hello, {props.name}!</p>;
}

export default function HelloWorld() {
    return (<>
        <Header />
        <h1 className="text-3xl text-center text-cyan-300 font-bold italic">Hello, World!</h1>
        <PropExample name="Lop" />
        <Link className='text-cyan-300 underline hover:text-cyan-500 block text-center' href="/">Go back to Home</Link>
    </>);
}