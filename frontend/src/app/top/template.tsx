import Header from "@/compornent/header";

const Template = ({ children }: { children: React.ReactNode }) => {
  return (
    <div>
      <Header></Header>
      {children}
    </div>
  );
};

export default Template;
